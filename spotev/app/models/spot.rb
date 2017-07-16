class Spot < ApplicationRecord

  def location_lat
    (location.include? '10') ? 33.127910519621246 : 33.127928489402585
  end

  def location_long
    (location.include? '10') ? -117.2653412793909 : -117.26436495530947
  end

  def free_count_report
    (location.include? '10') ? "There are #{bldg10_free_count} free spots" :
                               "There are #{bldg11_free_count} free spots"
  end

  def bldg10_free_count
    count = 0
    Spot.all.each { |s| count += 1 if (!s.occupied && s.location.include?('10')) }
    count
  end

  def bldg11_free_count
    count = 0
    Spot.all.each { |s| count += 1 if (!s.occupied && s.location.include?('11')) }
    count
  end

end
