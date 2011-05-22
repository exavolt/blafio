
import base

def main():
    print "Adding user..."
    success, user_data = base.add_user('TestUser1')
    assert success and user_data
    print "Adding app..."
    success, app_data = base.add_app('TestApp1')
    assert success and app_data
    print "Adding app access to the user..."
    success, app_user_data = base.add_app_user('TestApp1', 'TestUser1')
    assert success and app_user_data
    print "All OK!"

if __name__ == "__main__":
    main()
