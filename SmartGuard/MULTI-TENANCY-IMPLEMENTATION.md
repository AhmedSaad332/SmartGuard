# Smart Guard Multi-Tenancy Implementation

## نظرة عامة
هذا المستند يصف تنفيذ نظام الـ Multi-tenancy لنظام Smart Guard لضمان عزل البيانات بين المنظمات المختلفة.

## المشكلة الحالية
حالياً كل المنظمات تشوف نفس الأحداث في جدول واحد، وده غير آمن لمشروع Smart Guard.

## الحل المقترح
تنفيذ نظام Multi-tenancy كامل مع:

1. **Database Schema Update** - إضافة عمود org_id
2. **Detection Logic Update** - تضمين org_id في إنشاء الأحداث
3. **API Filtering** - فلترة الأحداث بناءً على المنظمة
4. **Supabase RLS** - سياسات أمان على مستوى الصفوف
5. **Frontend Integration** - تحديث الواجهة لاستخدام org_id

## الملفات المنفذة

### 1. Database Schema Migration
**ملف:** `supabase/migrations/add_org_id_to_events.sql`

```sql
-- Add org_id column as UUID type with foreign key constraint
ALTER TABLE events ADD COLUMN org_id UUID REFERENCES organizations(id);

-- Add index for better query performance
CREATE INDEX idx_events_org_id ON events(org_id);
```

**مميزات:**
- إضافة عمود org_id كـ UUID مع Foreign Key
- إنشاء index لتحسين الأداء
- تحديث البيانات الموجودة للتوافق
- إضافة عمود created_by للتتبع

### 2. Supabase Row Level Security (RLS)
**ملف:** `supabase/policies/events_rls.sql`

```sql
-- Enable RLS on events table
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Policy for organization-based access
CREATE POLICY "Users can view own organization events" ON events
    FOR SELECT USING (org_id = (SELECT org_id FROM users WHERE users.id = auth.uid()));
```

**مميزات:**
- تفعيل RLS على جدول events
- سياسات للقراءة والكتابة والتحديث والحذف
- عزل كامل للبيانات بين المنظمات
- دعم للمشرفين للوصول لكل البيانات

### 3. Backend API Enhancement
**ملف:** `backend/events_controller.py`

```python
@router.get("/events", response_model=List[EventResponse])
async def get_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    organization_id: Optional[str] = None
):
    # Apply organization filtering based on user role
    if current_user.role == "admin":
        # Admin can filter by specific organization
        if organization_id:
            query = query.filter(Event.org_id == uuid.UUID(organization_id))
    else:
        # Regular users only see their organization's events
        query = query.filter(Event.org_id == current_user.org_id)
```

**مميزات:**
- فلترة تلقائية بناءً على دور المستخدم
- دعم المشرفين لفلترة بالمنظمة
- تحقق من الصلاحيات للوصول للبيانات
- معالجة الأخطاء المناسبة

### 4. Frontend Detection Logic Update
**ملف:** `src/App.jsx`

```javascript
// Get current user's organization and org_id for event tracking
let eventOrganization = 'Unknown';
let orgId = null;
try {
  const currentUser = await authService.getCurrentUser();
  if (currentUser && currentUser.organization) {
    eventOrganization = currentUser.organization;
    orgId = currentUser.id; // Use user's org_id
  }
} catch (error) {
  console.error('Error getting user organization for event:', error);
}

const newEvent = {
  // ... other fields
  organization: eventOrganization, // Legacy organization name
  org_id: orgId // New org_id for multi-tenancy
};
```

**مميزات:**
- إضافة org_id لكل حدث جديد
- الحفاظة على التوافق مع الكود الحالي
- معالجة الأخطاء بشكل مناسب

### 5. Frontend Service Integration
**ملف:** `src/services/eventsService.js`

```javascript
export const getEvents = async (options = {}) => {
  const currentUser = await getCurrentUser();
  const params = new URLSearchParams();
  
  // Add organization filter for admin users
  if (currentUser.role === 'admin' && options.organizationId && options.organizationId !== 'all') {
    params.append('organization_id', options.organizationId);
  }
  
  const response = await fetch(`${API_BASE_URL}/events?${params.toString()}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  return await response.json();
};
```

**مميزات:**
- خدمة متكاملة للأحداث
- دعم الفلترة بالمنظمة
- معالجة المصادقة والصلاحيات
- دعم التصدير مع الفلترة

## خطوات التنفيذ

### 1. تنفيذ الـ Database Migration
```bash
# Connect to Supabase
psql -h [HOST] -U [USER] -d [DATABASE]

# Run migration
\i supabase/migrations/add_org_id_to_events.sql
```

### 2. تطبيق الـ RLS Policies
```bash
# Apply RLS policies
\i supabase/policies/events_rls.sql
```

### 3. تحديث الـ Backend
```bash
# Install dependencies
pip install fastapi sqlalchemy

# Update events controller
# Replace existing events controller with new implementation
```

### 4. تحديث الـ Frontend
```bash
# Add new service file
cp src/services/eventsService.js src/services/

# Update App.jsx to use org_id
# Modify event creation logic as shown above
```

## الفوائد المتوقعة

### 1. الأمان
- **عزل البيانات:** كل منظمة تشوف فقط بياناتها
- **منع الوصول الغير مصرح به:** RLS يمنع الوصول بين المنظمات
- **تدقيق الصلاحيات:** تحقق دقيق للوصول للبيانات

### 2. الأداء
- **تحسين الاستعلامات:** index على org_id يحسن الأداء
- **فلترة فعالة:** فلترة على مستوى قاعدة البيانات
- **تخزين مؤقت:** تحسينات للتخزين المؤقت

### 3. قابلية التوسع
- **سهولة الإضافة:** إضافة منظمات جديدة سهلة
- **مرونة الفلترة:** دعم متقدم للفلترة
- **توافقية:** الحفاظة على التوافق مع الأنظمة الحالية

## اختبار التنفيذ

### 1. اختبار العزل
```javascript
// Test 1: User from Org A cannot see Org B events
const userA = await login('userA@orgA.com', 'password');
const eventsA = await getEvents();
// Should only return Org A events

const userB = await login('userB@orgB.com', 'password');
const eventsB = await getEvents();
// Should only return Org B events
```

### 2. اختبار المشرفين
```javascript
// Test 2: Admin can filter by organization
const admin = await login('admin@smartguard.com', 'password');
const allEvents = await getEvents(); // All organizations
const orgAEvents = await getEvents({ organizationId: 'org-a-uuid' }); // Only Org A
```

### 3. اختبار الأمان
```sql
-- Test 3: Direct SQL access should be blocked
SELECT * FROM events; -- Should return only user's org events
INSERT INTO events (org_id, ...) VALUES ('other-org-uuid', ...); -- Should be blocked
```

## ملاحظات هامة

1. **النسخ الاحتياطي:** خذ نسخة احتياطية من قاعدة البيانات قبل التنفيذ
2. **الاختبار:** اختبر كل التغييرات في بيئة اختبار أولاً
3. **المراقبة:** راقب أداء النظام بعد التنفيذ
4. **التوثيق:** وثّق كل التغييرات والسياسات الجديدة

## الدعم الفني

لأي استفسارات فنية أو مشاكل في التنفيذ:

- **Database:** راسل فريق قاعدة البيانات
- **Backend:** تواصل مع فريق التطوير
- **Frontend:** ارجع للـ README في كل مكون

---

**تنفيذ:** Smart Guard Development Team  
**تاريخ:** 3 أبريل 2026  
**الإصدار:** v2.0 - Multi-Tenancy Release
