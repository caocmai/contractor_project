from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_car_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_car = {
        "model": "Model X",
        "cost": "40000",
        "url": "tesla.com"
}

sample_car_form = {
        "model": sample_car['model'],
        "cost": sample_car['cost'],
        "url": sample_car['url']
}


class CarTest(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the car homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Tesla Cars', result.data)

    def test_new(self):
        """Test the new car creation page."""
        result = self.client.get('/cars/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Model', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_car(self, mock_find):
        """Test showing a single car."""
        mock_find.return_value = sample_car

        result = self.client.get(f'/cars/{sample_car_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Model X', result.data)
        
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_car(self, mock_find):
        """Test editing a single car."""
        mock_find.return_value = sample_car

        result = self.client.get(f'/cars/edit/{sample_car_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Model X', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_car(self, mock_insert):
        """Test submitting a new car."""
        result = self.client.post('/new_car', data=sample_car_form)

        # After submitting, should redirect to that car
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_car)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_car(self, mock_update):
        result = self.client.post(f'/cars/{sample_car_id}', data=sample_car_form)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_car_id}, {'$set': sample_car})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_car(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/cars/{sample_car_id}/delete/', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_car_id})

if __name__ == '__main__':
    unittest_main()