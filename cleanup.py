from app import create_app
from extensions import db
from models import User, Company, Request, Device, CollectionPoint, RequestHistory

def cleanup():
    app = create_app()
    with app.app_context():
        company_ids = [2, 3, 4]
        user_ids = [5, 6, 8]
        
        # 1. Delete Devices and RequestHistory for Requests linked to these companies or users
        requests = Request.query.filter((Request.company_id.in_(company_ids)) | (Request.user_id.in_(user_ids))).all()
        request_ids = [r.request_id for r in requests]
        
        if request_ids:
            Device.query.filter(Device.request_id.in_(request_ids)).delete(synchronize_session=False)
            RequestHistory.query.filter(RequestHistory.request_id.in_(request_ids)).delete(synchronize_session=False)
            # Delete the Requests themselves
            Request.query.filter(Request.request_id.in_(request_ids)).delete(synchronize_session=False)

        # 2. Delete CollectionPoints linked to the companies
        CollectionPoint.query.filter(CollectionPoint.company_id.in_(company_ids)).delete(synchronize_session=False)
        
        # 3. Delete the Companies
        Company.query.filter(Company.company_id.in_(company_ids)).delete(synchronize_session=False)
        
        # 4. Delete the Users
        User.query.filter(User.user_id.in_(user_ids)).delete(synchronize_session=False)
        
        db.session.commit()
        print("Successfully cleaned up duplicates.")

if __name__ == '__main__':
    cleanup()
