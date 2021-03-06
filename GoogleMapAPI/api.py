__author__ = 'basnal'
from Actors.TimeKeeper import TimeKeeper
import googlemaps
import pprint


class GMap:
    PickUp = ""
    DropOff = ""
    MapService = googlemaps.Client(key='AIzaSyCb4y2S1BNpcTYtFjV9nd58N2E3etxe-O4')
    pp = pprint.PrettyPrinter(indent=2)
    time = TimeKeeper()

    def addLocations(self, locA, locB):
        self.PickUp = locA
        self.DropOff = locB

    def findRoute(self, origin, destination, mode):
        self.directions = self.MapService.directions(origin, destination,
                                                     mode=mode)

        #print ">>>>>>>>>> Directions"
        #self.pp.pprint(self.directions[0]['legs'][0])
        return self.directions[0]['legs'][0]

    def getGeocodeFor(self, location):
        res = self.MapService.geocode(location)
        self.pp.pprint(res[0]['formatted_address'])
        self.pp.pprint(res[0]['geometry']['location'])

        return [res[0]['geometry']['location']['lat'], res[0]['geometry']['location']['lng']]

    def findRouteofBus(self, bus):

        # The directions must be calculated with midways
        print bus.origin
        print bus.destination
        print "\n\nBus Route>>>"
        self.pp.pprint(bus.route)
        print "\n\n"

        self.directions = self.MapService.directions(bus.origin, bus.destination,
                                                     waypoints=bus.NewRoute,
                                                     mode='driving',
                                                     optimize_waypoints=True)

        # for total time self.directions[0]['legs'][0]['duration']
        #self.pp.pprint(self.directions)

        return self.directions

    def findRouteWithoutBus(self):
        if not self.PickUp or not self.DropOff:
            return

        self.PickUpGeocode = self.MapService.geocode(self.PickUp)
        self.DropOffGeocode = self.MapService.geocode(self.DropOff)

        # The directions must be calculated with midways
        self.directions = self.MapService.directions(self.PickUp, self.DropOff)


        # print self.directions[0]['legs'][0]['steps'][0]
        #for i in self.directions[0]['legs'][0]['steps'][0]:
            #print i

        return {'locations': {'origin': self.PickUpGeocode,
                              'destination': self.DropOffGeocode},
                'directions': self.directions}
