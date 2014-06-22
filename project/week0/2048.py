"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
import math
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies_generated = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        tmp_str = "\n"
        tmp_str +="Time:\t" + str(self._current_time) + "\n"
        tmp_str +="Cookies:\t" + str(self._current_cookies) + "\n"
        tmp_str +="Total Cookies:\t" + str(self._total_cookies_generated) + "\n"
        tmp_str +="CPS:\t" + str(self._current_cps) +"\n"
        tmp_str +="History:\t" + str(self._history[0]) + "..."+ str(self._history[len(self._history)-2]) + str(self._history[len(self._history)-1]) +"\n"
        return tmp_str
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0.0:
            self._current_time += time 
            self._current_cookies += time * self._current_cps
            self._total_cookies_generated += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies_generated))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    clicker_state = ClickerState()
    build_info_tmp = build_info.clone()
    item = ""
    while clicker_state.get_time() <= duration:
        item = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), duration - clicker_state.get_time(), build_info_tmp)
        if item == None:
            break
        time = clicker_state.time_until(build_info_tmp.get_cost(item))
        if clicker_state.get_time() + time > duration:
            break
        clicker_state.wait(time)
        clicker_state.buy_item(item, build_info_tmp.get_cost(item), build_info_tmp.get_cps(item))
        build_info_tmp.update_item(item)
    if clicker_state.get_time() < duration:
        clicker_state.wait(duration - clicker_state.get_time())
    return clicker_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    return the cheapest item
    """
    clicker_state = ClickerState()
    item_ch = build_info.build_items()[0]
    for item in build_info.build_items():
        if build_info.get_cost(item) < build_info.get_cost(item_ch):
            item_ch = item
    if (clicker_state.time_until(build_info.get_cost(item_ch)) > time_left):
        return None
    else:
        return item_ch
def time_to_wait(cookies, cps, cost):
    """
    dirty code
    """
    if cookies >= cost:
        return 0.0
    else:
        return math.ceil((cost - cookies) / cps)
    

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    return the most expensive item
    """
    index = 0
    item_ex = None
    while item_ex == None and index < len(build_info.build_items()):
        if time_to_wait(cookies, cps, build_info.get_cost(build_info.build_items()[index])) <= time_left:
            item_ex = build_info.build_items()[index]
            break
        index += 1
    if item_ex == None:
        return None
    for item in build_info.build_items():
        if build_info.get_cost(item) > build_info.get_cost(item_ex) and time_to_wait(cookies, cps, build_info.get_cost(item)) <= time_left:
            item_ex = item
    if (time_to_wait(cookies, cps, build_info.get_cost(item_ex)) > time_left):
        return None
    else:
        return item_ex

def strategy_best(cookies, cps, time_left, build_info):
    """
    return the best item
    """
    clicker_state = ClickerState()
    item_be = build_info.build_items()[0]
    expectation_be = (cps + build_info.get_cps(item_be)) * (time_left - time_to_wait(cookies, cps, build_info.get_cost(item_be))) + cps * time_to_wait(cookies, cps, build_info.get_cost(item_be))
    for item in build_info.build_items():
        expectation = (cps + build_info.get_cps(item)) * (time_left - time_to_wait(cookies, cps, build_info.get_cost(item))) + cps * time_to_wait(cookies, cps, build_info.get_cost(item))
        if expectation > expectation_be and clicker_state.time_until(build_info.get_cost(item_be)) < time_left:
            item_be = item
            expectation_be = expectation
    if (time_to_wait(cookies, cps, build_info.get_cost(item_be)) > time_left):
        return None
    else:
        return item_be
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it
    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 500, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)
    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()