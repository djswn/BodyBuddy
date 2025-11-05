class WeightAdjuster:
    def __init__(self, root, initial_weight):
        self.weight = initial_weight
        self.label = tk.Label(root, text=f"현재 체중: {self.weight}kg")
        self.label.pack()

        tk.Button(root, text="-", command=self.decrease).pack(side="left")
        tk.Button(root, text="+", command=self.increase).pack(side="right")

    def increase(self):
        self.weight += 1
        self.update_label()

    def decrease(self):
        self.weight -= 1
        self.update_label()

    def update_label(self):
        self.label.config(text=f"현재 체중: {self.weight}kg")
