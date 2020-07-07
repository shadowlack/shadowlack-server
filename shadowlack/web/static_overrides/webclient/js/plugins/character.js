let character_plugin = (function () {

  var init = function() {
    window.plugins['goldenlayout'].addKnownType('character');
  }

  var postInit = function() {
    var myLayout = window.plugins['goldenlayout'].getGL();

    // register our component and replace the default messagewindow
    myLayout.registerComponent('character_pane', function (container, componentState) {
        let mycssdiv = $('<div>').addClass('character_pane');
        mycssdiv.attr('types', 'character');
        mycssdiv.attr('update_method', 'newlines');
        mycssdiv.appendTo(container.getElement());
        console.log(container)
    });

    console.log("Character Pane Loaded");
  }

  return {
    init: init,
    postInit: postInit
  }
})();

window.plugin_handler.add("character", character_plugin);
