
import  os
import  uuid
def pathexce():
    base_path = os.path.join(os.getcwd(),'reportimg')
    report_only=uuid.uuid4().hex
    path=os.path.join(base_path,report_only)
    if not os.path.exists(path):
        os.makedirs(path)
    return path