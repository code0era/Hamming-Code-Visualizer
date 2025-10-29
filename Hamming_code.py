import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Color theme
COLORS = {
    'primary_bg': '#1a1d2e',
    'secondary_bg': '#16213e',
    'accent_blue': '#0f4c75',
    'light_bg': '#f5f7fa',
    'success': '#27ae60',
    'warning': '#f39c12',
    'highlight': '#3498db',
    'error_red': '#c0392b'
}

def calcRedundantBits(m):
    # Calculate the number of parity bits needed
    for i in range(m):
        if 2 ** i >= m + i + 1:
            return i

def posRedundantBits(data, r):
    # Insert parity bits at positions of power of 2
    j = 0
    k = 1
    m = len(data)
    res = ''
    for i in range(1, m + r + 1):
        if i == 2 ** j:
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1
    return res[::-1]

def calcParityBits(arr, r):
    n = len(arr)
    arr = list(arr)
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[-j])  # Reverse index
        arr[n - (2 ** i)] = str(val)
    return ''.join(arr)

def detectError(arr, nr):
    n = len(arr)
    res = 0
    for i in range(nr):
        val = 0
        for j in range(1, n + 1):
            if j & (2 ** i) == (2 ** i):
                val = val ^ int(arr[-j])
        res = res + val * (10 ** i)
    return int(str(res), 2)

class HammingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming Code Visualizer")
        self.root.geometry("1150x650")
        self.root.configure(bg=COLORS['primary_bg'])
        self.create_gui()
    
    def create_gui(self):
        main_frame = tk.Frame(self.root, bg=COLORS['primary_bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (input)
        left_panel = tk.Frame(main_frame, bg=COLORS['secondary_bg'], relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=8, ipadx=10, ipady=10)
        
        tk.Label(left_panel, text="HAMMING CODE", font=('Segoe UI', 16, 'bold'),
                 bg=COLORS['highlight'], fg='white').pack(fill=tk.X, pady=(5,10))
        
        tk.Label(left_panel, text="Enter Data Bits (e.g. 1011001):",
                 bg=COLORS['secondary_bg'], fg='white', font=('Segoe UI', 12)).pack(pady=(10,2), anchor='w')
        self.input_bitstring = tk.Entry(left_panel, font=('Consolas', 13), width=25,
                                       bg='white', fg=COLORS['primary_bg'])
        self.input_bitstring.pack(pady=(0,12), ipadx=8, ipady=4)
        
        self.encode_btn = tk.Button(left_panel, text="Generate Hamming Code",
                                    bg=COLORS['success'], fg='white', font=('Segoe UI', 12, 'bold'),
                                    command=self.calculate_hamming, padx=10, pady=5)
        self.encode_btn.pack(pady=(10,15))
        
        tk.Label(left_panel, text="Simulate Bit Error (0 = no error):",
                 bg=COLORS['secondary_bg'], fg='white', font=('Segoe UI', 10)).pack(pady=(20,2), anchor='w')
        self.error_pos = tk.Entry(left_panel, font=('Consolas', 12), width=12,
                                 bg='white', fg=COLORS['primary_bg'])
        self.error_pos.pack(pady=(0,12), ipadx=6, ipady=4)
        
        self.simulate_btn = tk.Button(left_panel, text="Simulate Transmission & Detect Error",
                                     bg=COLORS['warning'], fg='white', font=('Segoe UI', 11, 'bold'),
                                     command=self.simulate_error, padx=8, pady=5)
        self.simulate_btn.pack(pady=(5,15))
        
        self.clear_btn = tk.Button(left_panel, text="Clear All",
                                   bg=COLORS['error_red'], fg='white', font=('Segoe UI', 10, 'bold'),
                                   command=self.clear_all, padx=7, pady=4)
        self.clear_btn.pack(pady=(5,5))
        
        # Right panel (visualizations/output)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'))
        
        # Tab 1: Step-by-Step
        self.step_frame = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.step_frame, text='Step-by-Step')
        self.step_text = scrolledtext.ScrolledText(self.step_frame, font=('Consolas', 12),
                                                   bg=COLORS['light_bg'], fg=COLORS['primary_bg'],
                                                   relief=tk.GROOVE, borderwidth=1)
        self.step_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 2: Output
        self.result_frame = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.result_frame, text='Results')
        self.result_text = scrolledtext.ScrolledText(self.result_frame, font=('Consolas', 12),
                                                    bg=COLORS['light_bg'], fg=COLORS['primary_bg'],
                                                    relief=tk.GROOVE, borderwidth=1)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # State
        self.encoded = None
        self.r_bits = None
        
    def calculate_hamming(self):
        data = self.input_bitstring.get().strip()
        if not data or any(c not in "01" for c in data):
            messagebox.showerror("Input Error", "Please enter a valid bit string (0s and 1s only).")
            return
        m = len(data)
        r = calcRedundantBits(m)
        arranged = posRedundantBits(data, r)
        encoded = calcParityBits(arranged, r)
        self.encoded = encoded
        self.r_bits = r
        self.show_steps(data, arranged, encoded, r)
        self.show_results(data, encoded, None, None)
    
    def show_steps(self, data, arranged, encoded, r):
        self.step_text.configure(state='normal')
        self.step_text.delete("1.0", tk.END)
        self.step_text.insert(tk.END, f"Input Data Bits: {data}\n\n")
        self.step_text.insert(tk.END, f"Step 1: Calculate number of redundant (parity) bits needed\n")
        self.step_text.insert(tk.END, f"  -> r = {r}\n\n")
        self.step_text.insert(tk.END, f"Step 2: Place redundancy bits at positions: 1,2,4,8,...\n")
        self.step_text.insert(tk.END, f"  -> Data with parity bit positions: {arranged}\n\n")
        self.step_text.insert(tk.END, f"Step 3: Calculate values of parity bits for even parity\n")
        for i in range(r):
            covered = [j for j in range(1, len(encoded)+1) if j & (2**i)]
            self.step_text.insert(tk.END, f"  -> Parity bit {2**i} covers positions: {covered}\n")
        self.step_text.insert(tk.END, f"  -> Complete encoded message: {encoded}\n")
        self.step_text.configure(state='disabled')
    
    def show_results(self, data, encoded, error_idx, corrected):
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"Encoded Message for Transmission:\n  {encoded}\n\n", 'success')
        if error_idx is not None:
            self.result_text.insert(tk.END, f"Simulated Error - Bit flipped at position {error_idx}:\n", 'error')
            self.result_text.insert(tk.END, f"  Received Data: {corrected}\n")
            self.result_text.insert(tk.END, "Result of Error Detection and Correction:\n")
            pos_display = error_idx if error_idx != 0 else "None"
            self.result_text.insert(tk.END, f"  Error Detected at position: {pos_display}\n")
            if error_idx:
                self.result_text.insert(tk.END, f"  Corrected Data: {self.encoded}\n", 'success')
            else:
                self.result_text.insert(tk.END, "  No correction needed!\n")
        self.result_text.configure(state='disabled')
    
    def simulate_error(self):
        if not self.encoded or not self.r_bits:
            messagebox.showerror("Simulation Error", "Please generate Hamming code first.")
            return
        idx_str = self.error_pos.get().strip()
        if not idx_str.isdigit():
            messagebox.showerror("Input Error", "Enter error position (integer, 0 means no error).")
            return
        idx = int(idx_str)
        if idx == 0:
            error_data = self.encoded
        elif 1 <= idx <= len(self.encoded):
            # Flip bit at idx (1-based, left-to-right)
            ed = list(self.encoded)
            ed[idx - 1] = '1' if ed[idx - 1] == '0' else '0'
            error_data = ''.join(ed)
        else:
            messagebox.showerror("Input Error", f"Error position must be in the range 1..{len(self.encoded)} or 0.")
            return
        
        correction = detectError(error_data, self.r_bits)
        self.show_results(self.input_bitstring.get().strip(), self.encoded, correction, error_data)
    
    def clear_all(self):
        self.input_bitstring.delete(0, tk.END)
        self.error_pos.delete(0, tk.END)
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state='disabled')
        self.step_text.configure(state='normal')
        self.step_text.delete("1.0", tk.END)
        self.step_text.configure(state='disabled')
        self.encoded = None
        self.r_bits = None

if __name__ == "__main__":
    root = tk.Tk()
    app = HammingApp(root)
    root.mainloop()
