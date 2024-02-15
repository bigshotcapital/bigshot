from frappe.model.document import Document
import frappe 

class Connector(Document):
    def validate(self):
        if self.workflow_state == "Approved":
            self.create_user()

    def create_user(self):
        existing_user = frappe.get_all('User', filters={'email': self.email}, fields=['name'])
        
        if existing_user:
            return
        else:
            user = frappe.get_doc({
                'doctype': 'User',
                'email': self.email,
                'first_name': self.first_name if self.first_name else 'DefaultFirstName',
                'MobNo': self.mobno,
                'send_welcome_email': False,
                'roles': [{'roles': roles} for roles in self.roles.split(',')] if self.roles else None,
            })

            user.insert()
            
            frappe.msgprint(("User {0} created successfully.").format(user.name))
    
