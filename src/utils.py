def apply_action(driver, action):
    return driver.find_element(action[0], action[1])

def apply_actions(driver, actions):
    return list(map(lambda x: apply_action(driver, x), actions))