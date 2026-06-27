from models.audit_log_model import AuditLog
from models.order_model import Order
from models.payment_model import Payment

def create_auditlog(db,entity_type:str,entity_id:int,action:str,user_id:int = None,status_before :str=None, status_after:str = None, metadata:dict = None):
    
    
    log = AuditLog(entity_type= entity_type,
                   entity_id = entity_id,
                   action=action,
                   user_id = user_id,
                   status_before =status_before,
                   status_after= status_after,
                   details = metadata or {}
                   )
    db.add(log)
    