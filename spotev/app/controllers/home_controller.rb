class HomeController < ApplicationController

    def index
      @spots = Spot.all
    end
end
