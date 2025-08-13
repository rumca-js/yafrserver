function applyConfiguration() {
    view_display_style = "{user_config.display_style}";
    view_display_type = "{user_config.display_type}";
    view_show_icons = "{user_config.show_icons}" == "True";
    view_small_icons = "{user_config.small_icons}" == "True";
    debug = "{debug}" == "True";
    user_age = {user_config.get_age};

    setDisplayMode();
}

//-----------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    console.log("Initializing")

    getBasicPageElements();
    applyConfiguration();
 
    // TODO - this could spawn many requests - only if active?
    //setInterval(function() {
    //   getBasicPageElements();
    //}, 300000);
});


