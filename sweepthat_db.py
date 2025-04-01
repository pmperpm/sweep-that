import csv, os

class DB:
    def add_to_csv(self, date_start, react_time, cor_pos, cor_idx, clicked_pos, clicked_idx,rahu_pos, result):
        data = {
            'date_start' : date_start,
            'react_time': react_time,
            'cor_pos': cor_pos,
            'cor_idx': cor_idx,
            'clicked_pos': clicked_pos,
            'clicked_idx': clicked_idx,
            'rahu_pos': rahu_pos,
            'result': result
        }
        
        # File path
        csv_file = 'sweepthatDB.csv'
        
        # Write to CSV
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            
            # Write header if file is empty
            if file.tell() == 0:
                writer.writeheader()
                
            writer.writerow(data)