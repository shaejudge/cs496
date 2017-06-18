from google.appengine.ext import ndb

import webapp2
import json

class Boat(ndb.Model):
	#id = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty()
	length = ndb.IntegerProperty()
	at_Sea = ndb.BooleanProperty()
	
#class departure_history(ndb.Model):
	#departure_date = ndb.StringProperty()
	#departed_boat = ndb.StringProperty()
	
class Slip(ndb.Model):
	#id = ndb.StringProperty(required=True)
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	#departure_histories = ndb.StructuredProperty(departure_history, repeated=True)

class BoatHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_Sea=True)
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boats/' + new_boat.key.urlsafe()
		boat_dict['boat_id'] = new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))
		
	def get(self, id=None):
		if id: 
			b = ndb.Key(urlsafe=id).get()
			#b.length = 100
			#b.put()
			b_d = b.to_dict()
			b_d['self'] = '/boats/' + id
			#b_d['boat_id'] = id
			self.response.write(json.dumps(b_d))
			
	def delete(self, id=None):
		if id: 
			b_del = ndb.Key(urlsafe=id).get()
			b_del.key.delete()
			self.response.write("Slip Deleted")
			
	def patch(self, id=None):
		if id:
			newBoat_data = json.loads(self.request.body)
			b_patch = ndb.Key(urlsafe=id).get()
			b_patch.name = newBoat_data['name']
			b_patch.length = newBoat_data['length']
			b_patch.type = newBoat_data['type']
			b_patch.at_Sea = newBoat_data['at_Sea']
			b_patch.put()
			b_patch_dict = b_patch.to_dict()
			self.response.write(json.dumps(b_patch_dict))

			
	def put(self, id=None):
		if id:
			put_bdata = json.loads(self.request.body)
			d_put = ndb.Key(urlsafe=id).get()
			d_put.name=put_bdata['name']
			d_put.length=put_bdata['length']
			d_put.type=put_bdata['type']
			d_put.at_Sea=put_bdata['at_Sea']
			d_put.put()
			d_put_dict = d_put.to_dict()
			d_put_dict['self'] = '/boats/' + d_put.key.urlsafe()
			self.response.write(json.dumps(d_put_dict))
			self.response.write('\n')
			self.response.write(ndb.Key(urlsafe=id))
			
		
class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		new_slip = Slip(number=slip_data['number'], current_boat=None, arrival_date=None)
		new_slip.put()
		slip_dict = new_slip.to_dict()
		slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
		self.response.write(json.dumps(slip_dict))
		
	def get(self, id=None):
		if id: 
			s = ndb.Key(urlsafe=id).get()
			#f.length = 100
			#f.put()
			s_d = s.to_dict()
			s_d['self'] = '/slips/' + id
			self.response.write(json.dumps(s_d))

	def delete(self, id=None):
		if id: 
			s_del = ndb.Key(urlsafe=id).get()
			s_del.key.delete()
			
			self.response.write("Slip Deleted")
	
	def patch(self, id=None):
		if id:
			newSlip_data = json.loads(self.request.body)
			s_patch = ndb.Key(urlsafe=id).get()
			s_patch.number = newSlip_data['number']
			s_patch.put()
			s_patch_dict = s_patch.to_dict()
			self.response.write(json.dumps(s_patch_dict))
			
	def put(self, id=None):
		if id:
			put_data = json.loads(self.request.body)
			s_put = ndb.Key(urlsafe=id).get()
			s_put.number=put_data['number']
			s_put.current_boat= '/boats/' + put_data['current_boat']
			s_put.arrival_date=put_data['arrival_date']
			s_put.put()
			s_put_dict = s_put.to_dict()
			s_put_urlsafe = s_put.key.urlsafe()
			s_put_dict['self'] = '/slips/' + s_put_urlsafe
			
			if put_data['current_boat'] != None:
				b_put_here = (ndb.Key(urlsafe=put_data['current_boat'])).get()
				b_put_here.at_Sea = False
				b_put_here.put()
			
			self.response.write(json.dumps(s_put_dict))
			self.response.write(put_data['current_boat'])
			#self.response.write((ndb.Key(urlsafe=put_data['current_boat'])).get())
	
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write("Boats and Slips")
		
		
		
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH', ))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/boats', BoatHandler),
	('/boats/(.*)', BoatHandler),
	('/slips', SlipHandler),
	('/slips/(.*)/boats', SlipHandler),
	('/slips/(.*)', SlipHandler)
], debug=True)
