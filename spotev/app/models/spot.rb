class Spot < ApplicationRecord

  def location_lat
    self.location == 'building 10' ? 33.127910519621246 : 33.127928489402585
  end

  def location_long
    self.location == 'building 10' ? -117.2653412793909 : -117.26436495530947
  end

end
