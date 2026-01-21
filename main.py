import login
import dashboard

def open_dashboard(username, role):
    dashboard.open_dashboard(username, role)

if __name__ == "__main__":
    login.start_login(open_dashboard)
