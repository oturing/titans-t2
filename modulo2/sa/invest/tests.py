import unittest

from sqlalchemy import create_engine

from entities import Client

class TestDataLoad(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        models.Base.metadata.create_all(engine)

    def test_client(self):
        client = Client.fetch(tax_payer_id=1)
        assertEquals(client.name, 'Client One')
        assertEquals(client.address, 'Address One')

if __name__ == '__main__':
    unittest.main()
