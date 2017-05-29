Account type: [u'fraudster_event', u'premium', u'spammer_warn', u'fraudster',
       u'spammer_limited', u'spammer_noinvite', u'locked', u'tos_lock',
       u'tos_warn', u'fraudster_att', u'spammer_web', u'spammer']

Fraud (0): 13044
Not Fraud (1): 1293

create event_duration
drop event_end
drop event_start
convert acct_type to fraud/no fraud and drop acct_type
drop object_id
drop venue_name
drop venue_address
convert unpopular email_domain to other
for ticket_types, split into types_count, min_price, max_price, quantity_sold, quantity_total, value_sold, value_total and weighted_price
drop ticket_types
keep approx_payout_date
keep body_length
keep channels
keep country
keep currency
keep delivery method
do NLP on description and feed in single value
keep event_created
keep event_published
keep fb_published
keep gts
keep has_analytics
keep has_header
keep has_logo
do NLP on name and feed in single value
keep name_length
keep num_order
keep num_payouts
do NLP on org_desc and feed in single value
do NLP on org_name and feed in single value
keep org_facebook
keep org_twitter
convert payee_name to boolean [ 0 if payee_name doesn't exist, 1 if it does]
keep payout_type and enter 'not_available' for missing values
modify previous_payouts column to just be number of previous payouts
keep sale_duration
keep sale_duration2
keep show_map
keep user_age
drop user_created
keep user_type
keep venue_country
keep venue_state
drop venue_latitude
drop venue_longitude
