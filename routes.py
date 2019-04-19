from config import app
from controller_functions import register_login,create_new_user,bright_ideas,log_in,log_out,add_post,user,like,post,delete

#login/register page
app.add_url_rule("/",view_func = register_login)
app.add_url_rule("/users/create",view_func = create_new_user,methods=["POST"])
app.add_url_rule("/users/login",view_func = log_in,methods=["POST"])

#brigth idea page
app.add_url_rule("/bright_ideas",view_func = bright_ideas)
app.add_url_rule("/posts/create",view_func = add_post,methods=["POST"])
app.add_url_rule("/user/<user_id>",view_func = user)
app.add_url_rule("/bright_ideas/<post_id>/like",view_func = like)
app.add_url_rule("/bright_ideas/<post_id>",view_func = post)
app.add_url_rule("/posts/<post_id>/delete",view_func = delete)

#logout
app.add_url_rule("/logout",view_func = log_out)