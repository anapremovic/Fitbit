import database as db

def generate_active_min_to_sleep_min_regression():
    active_min_df = db.fetch_total_active_minutes_per_user_and_date()
    sleep_min_df = db.get_sleep_data()

    active_min_and_sleep_min_df = active_min_df.merge(sleep_min_df, on=['UserId', 'Date'])

    print(active_min_and_sleep_min_df)

generate_active_min_to_sleep_min_regression()
