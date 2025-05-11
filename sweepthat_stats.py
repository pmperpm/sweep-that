import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class Stats:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Statistics Visualizer")
        self.root.geometry("1400x900")
        
        # Load data (replace with your actual data loading)
        self.data = pd.read_csv("sweepthatDB.csv")
        # Convert date strings to datetime objects
        if 'date_start' in self.data.columns:
            self.data['date_start'] = pd.to_datetime(self.data['date_start'])
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main container
        self.mainframe = ttk.Frame(self.root, padding="20")
        self.mainframe.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        self.control_frame = ttk.Frame(self.mainframe)
        self.control_frame.pack(fill=tk.X, pady=10)
        
        # Graph selection
        ttk.Label(self.control_frame, text="Select Visualization:").pack(side=tk.LEFT)
        
        self.graph_var = tk.StringVar()
        self.graph_options = [
            "Success Rate: Hard vs Normal Mode (Histogram)",
            "Top 9 Longest Times Use to Clicked Card (Heatmap)",
            "Most Incorrect Clicked Position (Piechart)",
            "Rahu Position vs Correct Position Success Rates",
            "Reaction Times Over Sessions (Line Graph)",
            "Card that User doesn't Clicked Correctly (Histogram)"
        ]
        
        self.graph_menu = ttk.Combobox(
            self.control_frame,
            textvariable=self.graph_var,
            values=self.graph_options,
            state="readonly",
            width=40
        )
        self.graph_menu.pack(side=tk.LEFT, padx=10)
        self.graph_menu.current(0)
        
        # Plot button
        self.plot_btn = ttk.Button(
            self.control_frame,
            text="Generate Visualization",
            command=self.generate_visualization
        )
        self.plot_btn.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(self.control_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Visualization area
        self.viz_frame = ttk.Frame(self.mainframe)
        self.viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize with empty figure
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Table area 
        self.table_frame = ttk.Frame(self.viz_frame)
        self.text_widget = tk.Text(self.table_frame, wrap=tk.NONE)
        self.scroll_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scroll_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.generate_visualization()
    
    def generate_visualization(self):
        """Generate the selected visualization"""
        selected = self.graph_var.get()
        
        # Hide table and show canvas by default
        self.table_frame.pack_forget()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure.clear()
        
        try:
            if selected == self.graph_options[0]:
                self.plot_success_rates()
            elif selected == self.graph_options[1]:
                self.plot_reaction_time_heatmap()
            elif selected == self.graph_options[2]:
                self.plot_position_accuracy()
            elif selected == self.graph_options[3]:
                self.show_position_analysis()
            elif selected == self.graph_options[4]:
                self.plot_reaction_times()
            elif selected == self.graph_options[5]:
                self.plot_correct_positions()
            
            self.canvas.draw()
            self.status_label.config(text=f"Displaying: {selected}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
    
    def plot_success_rates(self):
        """Bar graph comparing success rates between hard and normal modes"""
        ax = self.figure.add_subplot(111)
        
        # Convert result to numeric (1 for CORRECT, 0 otherwise)
        self.data['result_numeric'] = self.data['result'].apply(
            lambda x: 1 if x == 'CORRECT' else 0
        )
        
        # Prepare data
        hard_mode = self.data[self.data['rahu_pos'].notna()]
        normal_mode = self.data[self.data['rahu_pos'].isna()]
        
        hard_success = hard_mode['result_numeric'].mean()
        normal_success = normal_mode['result_numeric'].mean()
        
        # bar plot
        bars = ax.bar(['Hard Mode', 'Normal Mode'], [hard_success, normal_success], 
                    color=['#ff7f0e', '#1f77b4'])
        ax.set_ylabel('Success Rate')
        ax.set_title('Comparison of Success Rates Between Game Modes')
        ax.set_ylim(0, 1)
        
        # Add value
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1%}', ha='center', va='bottom')
    
    def plot_reaction_time_heatmap(self):
        ax = self.figure.add_subplot(111)
        
        correct_clicks = self.data[self.data['result'] == 'CORRECT']
        reaction_stats = correct_clicks.groupby('clicked_idx')['react_time']\
            .agg(['mean', 'count'])\
            .rename(columns={'mean': 'avg_time', 'count': 'click_count'})
        
        top9 = reaction_stats.nlargest(9, 'avg_time')
        
        # 3x3 grid
        heatmap_data = pd.DataFrame(0, index=range(3), columns=range(3))
        card_labels = pd.DataFrame('', index=range(3), columns=range(3))
        
        #top 9 cards
        for position, (card_id, row) in enumerate(top9.iterrows()):
            row_idx = position // 3
            col_idx = position % 3
            heatmap_data.at[row_idx, col_idx] = row['avg_time']
            card_labels.at[row_idx, col_idx] = f"ID: {card_id}\n({row['avg_time']:.0f} ms)"
        
        sns.heatmap(
            heatmap_data,
            annot=card_labels.values,
            fmt='',
            cmap='YlOrRd',
            ax=ax,
            annot_kws={'size': 9, 'color': 'black', 'ha': 'center', 'va': 'center'},
            cbar_kws={'label': 'Average Reaction Time (ms)'},
            vmin=0,  # Ensure color scale starts at 0
            vmax=heatmap_data.max().max()  # Scale to the maximum reaction time
        )
        
        ax.set_title('Top 9 Cards with Longest Correct Reaction Times\n(Darker = Longer Time)', pad=20)
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')
        ax.set_xticklabels([1, 2, 3])
        ax.set_yticklabels([1, 2, 3])
        
        cbar = ax.collections[0].colorbar
        cbar.set_ticks(np.linspace(0, heatmap_data.max().max(), 5))
        
        plt.tight_layout()

    def plot_position_accuracy(self):
        """Pie chart showing which position types have most incorrect selections"""
        incorrect = self.data[
            (self.data['result'] == 'INCORRECT') | 
            (self.data['result'] == 'OPPO CORRECT')
        ]
        
        pos_counts = incorrect['cor_pos'].value_counts()
        
        all_pos = ['TOP LEFT', 'TOP RIGHT', 'MIDDLE LEFT', 
                        'MIDDLE RIGHT', 'BOTTOM LEFT', 'BOTTOM RIGHT']
        pos_counts = pos_counts.reindex(all_pos, fill_value=0)
        
        #color
        colors = plt.cm.Paired.colors[:6]
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        wedges, texts, autotexts = ax.pie(
            pos_counts,
            labels=pos_counts.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.8,
            textprops={'fontsize': 10}
        )
        
        ax.axis('equal')  
        ax.set_title('Incorrect Selections by Position Type', pad=20, fontsize=14)
        
        # autopct
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(10)
        
        # legend
        legend_labels = [f"{pos} ({count})" for pos, count in zip(pos_counts.index, pos_counts)]
        ax.legend(
            wedges,
            legend_labels,
            title="Position (Count)",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )
        
        self.figure.tight_layout()
        self.figure.canvas.draw()


    def show_position_analysis(self):
        """Table showing rahu position analysis with success rates"""
        # Clear previous widgets
        self.canvas.get_tk_widget().pack_forget()
        self.table_frame.pack(fill=tk.BOTH, expand=True)
            
        # treeview
        self.tree = ttk.Treeview(self.table_frame, columns=('Rahu Position', 'Correct Position', 'Success Rate'), 
                                show='headings', selectmode='browse')
        
        # columns
        self.tree.heading('Rahu Position', text='Rahu Position')
        self.tree.heading('Correct Position', text='Correct Position')
        self.tree.heading('Success Rate', text='Success Rate')
        
        self.tree.column('Rahu Position', width=150, anchor='center')
        self.tree.column('Correct Position', width=150, anchor='center')
        self.tree.column('Success Rate', width=150, anchor='center')
        
        # scrollbar
        y_scroll = ttk.Scrollbar(self.table_frame, orient='vertical', command=self.tree.yview)
        x_scroll = ttk.Scrollbar(self.table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scroll.grid(row=0, column=1, sticky='ns')
        x_scroll.grid(row=1, column=0, sticky='ew')
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        # success rate
        success_r = []

        grouped = self.data.groupby(['rahu_pos', 'cor_pos'])
        for (rahu_pos, cor_pos), group in grouped:
            total = len(group)
            correct = len(group[group['result'] == 'CORRECT'])
            success_rate = correct / total if total > 0 else 0
            
            success_r.append({
                'rahu_pos': 'None' if pd.isna(rahu_pos) else rahu_pos,
                'cor_pos': cor_pos,
                'success_rate': f"{success_rate:.1%}",
                'is_match': rahu_pos == cor_pos  # Add flag for matching positions
            })
        
        # sort
        success_r.sort(key=lambda x: float(x['success_rate'].strip('%'))/100, reverse=True)

        self.tree.tag_configure('match', foreground='red')
        
        # insert data
        for item in success_r:
            tags = ('match',) if item['is_match'] else ()
            self.tree.insert('', 'end', 
                            values=(item['rahu_pos'], item['cor_pos'], item['success_rate']),
                            tags=tags)
        
        self.status_label.config(text="Displaying: Position Analysis Table")
    
    def plot_reaction_times(self):
        ax = self.figure.add_subplot(111)
        
        reacttime = self.data[
            (self.data['result'] == 'CORRECT') & 
            (self.data['react_time'] > 0)
        ].copy() 
        
        # sort
        data = reacttime.sort_values('date_start')
        
        # group data
        data['round_num'] = data['date_start'].ne(data['date_start'].shift()).cumsum()
        data['attempt_num'] = data.groupby('round_num').cumcount() + 1
        
        # x axis
        data['x_label'] = data.apply(
            lambda row: f"{row['round_num']} - {row['attempt_num']}", 
            axis=1
        )
        
        x_values = range(len(data))
        
        ax.plot(x_values, data['react_time'], 
            marker='o', linestyle='-', color='#2ca02c')
        # make it wider
        ax.margins(y=0.3)
        
        # label
        ax.set_xlabel('Game Round and Attempt')
        ax.set_ylabel('Reaction Time (ms)')
        ax.set_title('Reaction Times by Game Round (Correct Attempts Only)')
        ax.grid(True)
        
        # xticks
        ax.set_xticks(x_values)
        ax.set_xticklabels(data['x_label'], rotation=45, ha='right')
        
        # average line
        avg_time = data['react_time'].mean()
        ax.axhline(avg_time, color='r', linestyle='--', 
                label=f'Average: {avg_time:.2f}ms')
        ax.legend()
        
        self.figure.tight_layout()
        
    def plot_correct_positions(self):
        """Histogram showing frequency of incorrect cards including position 0 clicks"""
        ax = self.figure.add_subplot(111)
        
        # Filter for incorrect selections (either wrong card or clicked position 0)
        incorrect_selections = self.data[
            (self.data['cor_idx'] != self.data['clicked_idx']) | 
            (self.data['clicked_idx'] == 0)
        ]
        
        # Create position range (0-36)
        positions = range(0, 37)  # Include position 0
        
        # Count incorrect selections per card (using clicked_idx)
        freq = incorrect_selections['cor_idx'].value_counts()\
            .reindex(positions, fill_value=0)\
            .sort_index()
        
        # Create bar plot
        bars = ax.bar(
            freq.index,
            freq.values,
            color='#9467bd',  # Purple color
            edgecolor='black',
            alpha=0.7,
            width=0.8
        )
        
        # Customize plot
        ax.set_xlabel('Card Number (0-36)')
        ax.set_ylabel('Frequency')
        ax.set_title("Frequency of Card that user can't click correctly")
        ax.set_xticks(positions[::2])  # Show every other position to avoid crowding
        ax.set_xlim(-0.5, 36.5)  # Adjust to include position 0
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels for non-zero bars
        for i, bar in enumerate(bars):
            if bar.get_height() > 0 and i != 0:  # Skip label for position 0 (we already labeled it)
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.1,
                    f'{int(bar.get_height())}',
                    ha='center',
                    va='bottom'
                )
        
        self.figure.tight_layout()

if __name__ == "__main__":
    root = tk.Tk()
    app = Stats(root)
    root.mainloop()
