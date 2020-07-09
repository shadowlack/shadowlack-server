let character_pane = (function () {
  var postInit = function() {
    var myLayout = window.plugins['goldenlayout'].getGL();

    // register our component
    myLayout.registerComponent('character_pane', function (container, componentState) {
      let mycssdiv = $('<div>').addClass('content character');
        mycssdiv.attr('types', 'character');
        mycssdiv.attr('updateMethod', 'replace');
        mycssdiv.appendTo(container.getElement());
    });

    console.log("Character Pane Initialized.");
  }
  
  return {
    init: function () {},
    postInit: postInit
  }
})();

let inventory_pane = (function () {
  var postInit = function() {
    var myLayout = window.plugins['goldenlayout'].getGL();

    // register our component
    myLayout.registerComponent('inventory_pane', function (container, componentState) {
        let mycssdiv = $('<div>').addClass('content character');
        mycssdiv.attr('types', 'inventory');
        mycssdiv.attr('updateMethod', 'replace');
        mycssdiv.appendTo(container.getElement());
    });

    console.log("Inventory Pane Initialized.");
  }
  
  return {
    init: function () {},
    postInit: postInit
  }
})();

window.plugin_handler.add("character_pane", character_pane);
window.plugin_handler.add("inventory_pane", inventory_pane);
