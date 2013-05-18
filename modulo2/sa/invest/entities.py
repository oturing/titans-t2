import models

class Client():
    @classmethod
    def fetch(self, id=None, tax_payer_id=None):
        if id:
            return models.ClientTable.query.filter_by(
                    id=id).one()
        else:
            return models.ClientTable.query.filter_by(
                    tax_payer_id=tax_payer_id).one()

