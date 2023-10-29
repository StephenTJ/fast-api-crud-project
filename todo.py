import db


def add_todo_item(user_name, item_title, item_discription):
    add_todo_item_query = "INSERT INTO todo_items(item_title,item_discription,user_name,created_on) VALUES('"+str(
        item_title)+"','"+str(item_discription)+"','"+str(user_name)+"',now());"
    result = db.perform_iud_operation(add_todo_item_query)
    return result


def delete_todo_item(user_name, item_id):
    delete_todo_item_query = "DELETE FROM todo_items WHERE item_id='" + \
        str(item_id)+"' and user_name ilike '"+str(user_name)+"';"
    result = db.perform_iud_operation(delete_todo_item_query)
    return result


def update_todo_item(user_name, item_id, item_title, item_discription):
    update_todo_item_query = "UPDATE todo_items SET item_title='"+str(item_title)+"',item_discription='"+str(
        item_discription)+"' WHERE item_id='"+str(item_id)+"' and user_name ilike '"+str(user_name)+"';"
    result = db.perform_iud_operation(update_todo_item_query)
    return result


def get_todo_items(user_name):
    get_todo_items_query = "SELECT item_id,item_title, item_discription FROM todo_items WHERE user_name='" + \
        str(user_name)+"' ORDER BY created_on desc;"
    result = db.perform_select_operation(get_todo_items_query)
    return result
