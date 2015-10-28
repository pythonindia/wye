def get_message(context):
    workshop = context.get('workshop', None)

    if workshop:
        return construct_message(workshop, context)
    else:
        # Other messages for non-workshop creation actions
        return None


def construct_message(workshop, context):
    date = workshop.expected_date
    topic = workshop.workshop_section
    organization = workshop.requester
    workshop_url = context.get('workshop_url', None)
    message = "{} workshop at {} on {} confirmed! Details at {}".format(
        topic, organization, date, workshop_url)
    if len(message) >= 140:
        message = "{} workshop on {} confirmed! Details at {}".format(
            topic, date, workshop_url)

    return message
