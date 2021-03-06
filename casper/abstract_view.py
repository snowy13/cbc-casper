"""The view module ... """
from casper.justification import Justification


class AbstractView(object):
    """A set of seen messages. For performance, also stores a dict of most recent messages."""
    def __init__(self, messages=None):
        # now for some assignment...
        if messages is None:
            messages = set()

        self.add_messages(messages)

        self.messages = set()
        self.latest_messages = dict()

    def __str__(self):
        output = "View: \n"
        for bet in self.messages:
            output += str(bet) + "\n"
        return output

    def justification(self):
        """Returns the latest messages seen from other validators, to justify estimate."""
        return Justification(self.latest_messages)

    def get_new_messages(self, showed_messages):
        """This method returns the set of messages out of showed_messages
        and their dependency that isn't part of the view."""

        new_messages = set()
        # The memo will keep track of messages we've already looked at, so we don't redo work.
        memo = set()

        # At the start, our working set will be the "showed messages" parameter.
        current_set = set(showed_messages)
        while current_set != set():

            next_set = set()
            # If there's no message in the current working set.
            for message in current_set:

                # Which we haven't seen it in the view or during this loop.
                if message not in self.messages and message not in memo:

                    # But if we do have a new message, then we add it to our pile..
                    new_messages.add(message)

                    # and add the bet in its justification to our next working set
                    for bet in message.justification.latest_messages.values():
                        next_set.add(bet)
                    # Keeping a record of very message we inspect, being sure not
                    # to do any extra (exponential complexity) work.
                    memo.add(message)

            current_set = next_set

        # After the loop is done, we return a set of new messages.
        return new_messages

    def estimate(self):
        '''Must be defined in child class.
        Returns estimate based on current messages in the view'''
        pass

    def add_messages(self, showed_messages):
        '''Must be defined in child class.'''
        pass

    def make_new_message(self, validator):
        '''Must be defined in child class.'''
        pass

    def update_safe_estimates(self, validator_set):
        '''Must be defined in child class.'''
        pass
