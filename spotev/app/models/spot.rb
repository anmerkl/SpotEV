class Spot < ApplicationRecord

  def location_lat
    (location.include? '10') ? 33.127910519621246 : 33.127928489402585
  end

  def location_long
    (location.include? '10') ? -117.2653412793909 : -117.26436495530947
  end

  def occupied_str
    (occupied) ? 'Occupied' : 'Free'
  end

  def duration_to_min
    (prev_occupy_duration / 60).ceil
  end

  def to_str
    "Spot #{location}: #{occupied_str} - previously occupied for #{duration_to_min} minutes."
  end

  def bldg10_spots
    unique_spots = Spot.all.reverse.uniq { |s| s.location }
    bldg10_spots = unique_spots.select { |u| u.location.include?('10') }
    bldg10_spots
  end

  def free_bldg10_spots_count
    count = 0
    bldg10_spots.select { |f| count += 1 unless f.occupied }
    count
  end

  def bldg11_spots
    unique_spots = Spot.all.uniq { |s| s.location }
    bldg11_spots = unique_spots.select { |u| u.location.include?('11') }
    bldg11_spots
  end

  def free_bldg11_spots_count
    count = 0
    bldg11_spots.select { |f| count += 1 unless f.occupied }
    count
  end

  def spots_report
    report = ''
    if location.include?('10')
      report += "Free spots: #{free_bldg10_spots_count}\n"
      # bldg10_spots.each do |s|
      #   report += "#{s.to_str}\n"
      # end
    else
      report += "Free spots: #{free_bldg11_spots_count}\n"
      # bldg11_spots.each do |s|
      #   report += "#{s.to_str}\n"
      # end
    end
    report
  end

end
