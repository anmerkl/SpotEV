class HomeController < ApplicationController

    def index
      @spots = Spot.all
      @hash = Gmaps4rails.build_markers(@spots) do |spot, marker|
        marker.lat spot.location_lat
        marker.lng spot.location_long
        marker.infowindow spot.free_count_report
      end
    end
end
