/*
 *
 * Evennia Webclient help plugin
 *
 */
let clienthelp_plugin = (function () {

    var onOptionsUI = function (parentdiv) {
        var help_text = $([
            "<div class='client-settings'>",
                "<b>Web Client Settings</b>",
            "</div>"
        ].join(""));
        parentdiv.append(help_text);
    }

    return {
        init: function () {},
        onOptionsUI: onOptionsUI,
    }
})();

window.plugin_handler.add("clienthelp", clienthelp_plugin);
