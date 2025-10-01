class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("로그인")

        tk.Label(root, text="아이디").grid(row=0, column=0)
        tk.Label(root, text="비밀번호").grid(row=1, column=0)

        self.entry_id = tk.Entry(root)
        self.entry_pw = tk.Entry(root, show="*")
        self.entry_id.grid(row=0, column=1)
        self.entry_pw.grid(row=1, column=1)

        tk.Button(root, text="로그인", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        user_id = self.entry_id.get()
        pw = self.entry_pw.get()
        # 실제 구현에서는 DB/파일 검증 필요
        if user_id and pw:
            self.on_login_success(user_id)
        else:
            messagebox.showerror("오류", "아이디와 비밀번호를 입력하세요.")
