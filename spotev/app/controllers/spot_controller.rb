class SpotController < ApplicationController
  skip_before_action :verify_authenticity_token

  def create
    @spot = Spot.new(spot_params)
    @spot.save
  end

  def update
    @spot = Spot.update(spot_params)
  end

  private

    def spot_params
      params.require(:spot).permit(:location, :occupied, :prev_occupy_duration)
    end
end
