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
    """Returns error position and step-by-step syndrome calculation"""
    n = len(arr)
    syndrome_steps = []
    syndrome_bits = []
    
    for i in range(nr):
        parity_pos = 2 ** i
        val = 0
        covered_positions = []
        covered_bits = []
        
        for j in range(1, n + 1):
            if j & parity_pos == parity_pos:
                covered_positions.append(j)
                covered_bits.append(arr[-j])
                val = val ^ int(arr[-j])
        
        syndrome_bits.append(str(val))
        syndrome_steps.append({
            'parity_position': parity_pos,
            'covered_positions': covered_positions,
            'covered_bits': covered_bits,
            'syndrome_bit': val
        })
    
    # Calculate error position from syndrome
    res = 0
    for i in range(nr):
        res = res + int(syndrome_bits[i]) * (10 ** i)
    error_position = int(str(res), 2)
    
    return error_position, syndrome_steps, syndrome_bits


class HammingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamming Code Visualizer")
        self.root.geometry("1200x700")
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
                 bg=COLORS['secondary_bg'], fg='white', font=('Segoe UI', 12)).pack(pady=(10,2), anchor='w', padx=10)
        self.input_bitstring = tk.Entry(left_panel, font=('Consolas', 13), width=25,
                                       bg='white', fg=COLORS['primary_bg'])
        self.input_bitstring.pack(pady=(0,12), padx=10, ipadx=8, ipady=4)
        
        self.encode_btn = tk.Button(left_panel, text="Generate Hamming Code",
                                    bg=COLORS['success'], fg='white', font=('Segoe UI', 12, 'bold'),
                                    command=self.calculate_hamming, padx=10, pady=5)
        self.encode_btn.pack(pady=(10,15), padx=10, fill=tk.X)
        
        tk.Label(left_panel, text="Simulate Bit Error (0 = no error):",
                 bg=COLORS['secondary_bg'], fg='white', font=('Segoe UI', 10)).pack(pady=(20,2), anchor='w', padx=10)
        self.error_pos = tk.Entry(left_panel, font=('Consolas', 12), width=12,
                                 bg='white', fg=COLORS['primary_bg'])
        self.error_pos.pack(pady=(0,12), padx=10, ipadx=6, ipady=4)
        
        self.simulate_btn = tk.Button(left_panel, text="Simulate & Detect Error",
                                     bg=COLORS['warning'], fg='white', font=('Segoe UI', 11, 'bold'),
                                     command=self.simulate_error, padx=8, pady=5)
        self.simulate_btn.pack(pady=(5,15), padx=10, fill=tk.X)
        
        self.clear_btn = tk.Button(left_panel, text="Clear All",
                                   bg=COLORS['error_red'], fg='white', font=('Segoe UI', 10, 'bold'),
                                   command=self.clear_all, padx=7, pady=4)
        self.clear_btn.pack(pady=(5,5), padx=10, fill=tk.X)
        
        # Right panel (visualizations/output)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'))
        
        # Tab 1: Step-by-Step Encoding
        self.step_frame = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.step_frame, text='📝 Encoding Steps')
        self.step_text = scrolledtext.ScrolledText(self.step_frame, font=('Consolas', 11),
                                                   bg=COLORS['light_bg'], fg=COLORS['primary_bg'],
                                                   relief=tk.GROOVE, borderwidth=1, wrap=tk.WORD)
        self.step_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 2: Error Detection Steps
        self.detection_frame = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.detection_frame, text='🔍 Detection Steps')
        self.detection_text = scrolledtext.ScrolledText(self.detection_frame, font=('Consolas', 11),
                                                       bg=COLORS['light_bg'], fg=COLORS['primary_bg'],
                                                       relief=tk.GROOVE, borderwidth=1, wrap=tk.WORD)
        self.detection_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 3: Final Results
        self.result_frame = tk.Frame(self.notebook, bg=COLORS['light_bg'])
        self.notebook.add(self.result_frame, text='✅ Results')
        self.result_text = scrolledtext.ScrolledText(self.result_frame, font=('Consolas', 12),
                                                    bg=COLORS['light_bg'], fg=COLORS['primary_bg'],
                                                    relief=tk.GROOVE, borderwidth=1, wrap=tk.WORD)
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
        self.show_results(data, encoded, None, None, None)
        
        # Clear detection tab
        self.detection_text.configure(state='normal')
        self.detection_text.delete("1.0", tk.END)
        self.detection_text.insert(tk.END, "Generate error simulation to see detection steps...")
        self.detection_text.configure(state='disabled')
    
    def show_steps(self, data, arranged, encoded, r):
        self.step_text.configure(state='normal')
        self.step_text.delete("1.0", tk.END)
        
        self.step_text.insert(tk.END, "="*70 + "\n")
        self.step_text.insert(tk.END, "HAMMING CODE ENCODING - STEP BY STEP\n")
        self.step_text.insert(tk.END, "="*70 + "\n\n")
        
        self.step_text.insert(tk.END, f"Input Data Bits: {data}\n")
        self.step_text.insert(tk.END, f"Data length (m): {len(data)} bits\n\n")
        
        self.step_text.insert(tk.END, f"Step 1: Calculate number of parity bits needed\n")
        self.step_text.insert(tk.END, f"-"*70 + "\n")
        self.step_text.insert(tk.END, f"Formula: 2^r >= m + r + 1\n")
        self.step_text.insert(tk.END, f"Where m = {len(data)} (data bits)\n")
        self.step_text.insert(tk.END, f"Result: r = {r} parity bits needed\n")
        self.step_text.insert(tk.END, f"Total bits = {len(data)} + {r} = {len(encoded)}\n\n")
        
        self.step_text.insert(tk.END, f"Step 2: Position parity bits at powers of 2\n")
        self.step_text.insert(tk.END, f"-"*70 + "\n")
        self.step_text.insert(tk.END, f"Parity bits at positions: 1, 2, 4, 8, ...\n")
        self.step_text.insert(tk.END, f"Data with placeholders: {arranged}\n\n")
        
        self.step_text.insert(tk.END, f"Step 3: Calculate parity bit values (even parity)\n")
        self.step_text.insert(tk.END, f"-"*70 + "\n")
        
        for i in range(r):
            parity_pos = 2**i
            covered = [j for j in range(1, len(encoded)+1) if j & parity_pos]
            bits_at_pos = [encoded[-j] for j in covered]
            self.step_text.insert(tk.END, f"\nParity bit P{parity_pos} (position {parity_pos}):\n")
            self.step_text.insert(tk.END, f"  Covers positions: {covered}\n")
            self.step_text.insert(tk.END, f"  Bits at positions: {bits_at_pos}\n")
            self.step_text.insert(tk.END, f"  XOR result: {encoded[len(encoded)-parity_pos]}\n")
        
        self.step_text.insert(tk.END, f"\n" + "="*70 + "\n")
        self.step_text.insert(tk.END, f"Complete encoded message: {encoded}\n")
        self.step_text.insert(tk.END, "="*70 + "\n")
        self.step_text.configure(state='disabled')
    
    def show_detection_steps(self, received_data, error_pos, syndrome_steps, syndrome_bits):
        """Show detailed error detection steps"""
        self.detection_text.configure(state='normal')
        self.detection_text.delete("1.0", tk.END)
        
        self.detection_text.insert(tk.END, "="*70 + "\n")
        self.detection_text.insert(tk.END, "ERROR DETECTION - SYNDROME CALCULATION\n")
        self.detection_text.insert(tk.END, "="*70 + "\n\n")
        
        self.detection_text.insert(tk.END, f"Received Data: {received_data}\n\n")
        
        self.detection_text.insert(tk.END, "Step 1: Calculate Syndrome Bits\n")
        self.detection_text.insert(tk.END, "-"*70 + "\n")
        self.detection_text.insert(tk.END, "Recalculate each parity bit and check for errors:\n\n")
        
        for step in syndrome_steps:
            parity_pos = step['parity_position']
            covered = step['covered_positions']
            bits = step['covered_bits']
            syndrome_bit = step['syndrome_bit']
            
            self.detection_text.insert(tk.END, f"Parity Check P{parity_pos} (position {parity_pos}):\n")
            self.detection_text.insert(tk.END, f"  Covers positions: {covered}\n")
            self.detection_text.insert(tk.END, f"  Bits at positions: {bits}\n")
            self.detection_text.insert(tk.END, f"  XOR calculation: {' ⊕ '.join(bits)} = {syndrome_bit}\n")
            self.detection_text.insert(tk.END, f"  Syndrome bit S{parity_pos}: {syndrome_bit}\n\n")
        
        self.detection_text.insert(tk.END, "Step 2: Form Syndrome Vector\n")
        self.detection_text.insert(tk.END, "-"*70 + "\n")
        syndrome_vector = ''.join(reversed(syndrome_bits))
        self.detection_text.insert(tk.END, f"Syndrome bits (from right to left): {' '.join(syndrome_bits)}\n")
        self.detection_text.insert(tk.END, f"Syndrome vector (binary): {syndrome_vector}\n")
        self.detection_text.insert(tk.END, f"Syndrome value (decimal): {error_pos}\n\n")
        
        self.detection_text.insert(tk.END, "Step 3: Interpret Result\n")
        self.detection_text.insert(tk.END, "-"*70 + "\n")
        if error_pos == 0:
            self.detection_text.insert(tk.END, "✓ Syndrome = 0: No error detected!\n")
            self.detection_text.insert(tk.END, "  The received message is correct.\n")
        else:
            self.detection_text.insert(tk.END, f"✗ Syndrome = {error_pos}: Error detected!\n")
            self.detection_text.insert(tk.END, f"  Error is at position {error_pos} (from right, 1-indexed)\n")
            self.detection_text.insert(tk.END, f"  Corresponding to bit index {len(received_data) - error_pos + 1} (from left)\n\n")
            
            # Show correction
            corrected = list(received_data)
            corrected[-error_pos] = '1' if corrected[-error_pos] == '0' else '0'
            self.detection_text.insert(tk.END, "Step 4: Correct the Error\n")
            self.detection_text.insert(tk.END, "-"*70 + "\n")
            self.detection_text.insert(tk.END, f"Original bit at position {error_pos}: {received_data[-error_pos]}\n")
            self.detection_text.insert(tk.END, f"Corrected bit at position {error_pos}: {corrected[-error_pos]}\n")
            self.detection_text.insert(tk.END, f"Corrected message: {''.join(corrected)}\n")
        
        self.detection_text.insert(tk.END, "\n" + "="*70 + "\n")
        self.detection_text.configure(state='disabled')
    
    def show_results(self, data, encoded, error_idx, corrected, syndrome_info):
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, "HAMMING CODE - FINAL RESULTS\n")
        self.result_text.insert(tk.END, "="*70 + "\n\n")
        
        self.result_text.insert(tk.END, f"Original Data: {data}\n")
        self.result_text.insert(tk.END, f"Encoded Message: {encoded}\n\n")
        
        if error_idx is not None:
            self.result_text.insert(tk.END, "TRANSMISSION SIMULATION\n")
            self.result_text.insert(tk.END, "-"*70 + "\n")
            
            if error_idx == 0:
                self.result_text.insert(tk.END, f"Received Data: {corrected}\n")
                self.result_text.insert(tk.END, "Error Simulation: None (perfect transmission)\n\n")
                self.result_text.insert(tk.END, "DETECTION RESULT: ✓ No errors detected\n")
            else:
                # Show where error was introduced
                sent_visual = list(encoded)
                recv_visual = list(corrected)
                error_bit_idx = len(encoded) - error_idx
                
                self.result_text.insert(tk.END, f"Sent:     {encoded}\n")
                self.result_text.insert(tk.END, f"Received: {corrected}\n")
                self.result_text.insert(tk.END, f"Error introduced at position {error_idx} (from right)\n\n")
                
                self.result_text.insert(tk.END, f"DETECTION RESULT: ✗ Error at position {error_idx}\n")
                
                # Show correction
                corrected_msg = list(corrected)
                corrected_msg[-error_idx] = '1' if corrected_msg[-error_idx] == '0' else '0'
                self.result_text.insert(tk.END, f"Corrected Message: {''.join(corrected_msg)}\n")
                self.result_text.insert(tk.END, f"\n✓ Successfully corrected single-bit error!\n")
        
        self.result_text.insert(tk.END, "\n" + "="*70 + "\n")
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
        
        # Detect error with detailed steps
        error_position, syndrome_steps, syndrome_bits = detectError(error_data, self.r_bits)
        
        # Show detection steps in dedicated tab
        self.show_detection_steps(error_data, error_position, syndrome_steps, syndrome_bits)
        
        # Show final results
        self.show_results(self.input_bitstring.get().strip(), self.encoded, 
                         error_position, error_data, syndrome_steps)
        
        # Switch to detection tab to show the steps
        self.notebook.select(1)
    
    def clear_all(self):
        self.input_bitstring.delete(0, tk.END)
        self.error_pos.delete(0, tk.END)
        
        self.result_text.configure(state='normal')
        self.result_text.delete("1.0", tk.END)
        self.result_text.configure(state='disabled')
        
        self.step_text.configure(state='normal')
        self.step_text.delete("1.0", tk.END)
        self.step_text.configure(state='disabled')
        
        self.detection_text.configure(state='normal')
        self.detection_text.delete("1.0", tk.END)
        self.detection_text.configure(state='disabled')
        
        self.encoded = None
        self.r_bits = None


if __name__ == "__main__":
    root = tk.Tk()
    app = HammingApp(root)
    root.mainloop()
