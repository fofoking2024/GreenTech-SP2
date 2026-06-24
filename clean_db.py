# -*- coding: utf-8 -*-
"""
سكريبت لحذف جميع البيانات من قاعدة البيانات
وإعادة التسجيل من جديد
"""

from app import app
from extensions import db
from sqlalchemy import text

def reset_database():
    with app.app_context():
        print("⏳ جاري حذف البيانات...")
        
        # تعطيل قيود المفاتيح الخارجية مؤقتاً (لـ MySQL)
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # حذف البيانات من جميع الجداول
        tables = [
            "request_history",
            "device", 
            "request",
            "collectionpoint",
            "company",
            "user"
        ]
        
        for table in tables:
            try:
                db.session.execute(text(f"DELETE FROM `{table}`"))
                # إعادة تعيين العداد (AUTO_INCREMENT)
                db.session.execute(text(f"ALTER TABLE `{table}` AUTO_INCREMENT = 1"))
                print(f"  ✅ تم حذف بيانات جدول: {table}")
            except Exception as e:
                print(f"  ⚠️ خطأ في جدول {table}: {e}")
        
        # إعادة تفعيل قيود المفاتيح الخارجية
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        
        db.session.commit()
        print("\n✅ تم حذف جميع الحسابات والبيانات بنجاح!")
        print("🔄 يمكنك الآن إعادة التسجيل من جديد.")

if __name__ == "__main__":
    confirm = input("هل أنت متأكد من حذف جميع البيانات؟ (yes/no): ")
    if confirm.lower() in ["yes", "y", "نعم"]:
        reset_database()
    else:
        print("❌ تم الإلغاء.")

