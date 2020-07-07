/*
 *
 * Evennia Webclient help plugin
 *
 */
let clienthelp_plugin = (function () {

    var onOptionsUI = function (parentdiv) {
        var help_text = $( [
            "<div style='font-weight: bold;'>",
                "<a href='https://shadowlack.com'>Shadowlack</a>",
                " Web Client Settings:",
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
