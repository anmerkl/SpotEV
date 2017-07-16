class CreateSpots < ActiveRecord::Migration[5.1]
  def change
    create_table :spots do |t|
      t.string :location
      t.boolean :occupied
      t.float :prev_occupy_duration

      t.timestamps
    end
  end
end
