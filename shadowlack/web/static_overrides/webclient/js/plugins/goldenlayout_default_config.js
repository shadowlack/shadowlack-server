var goldenlayout_config = {
  dimensions: {},
  content: [{
    type: 'column',
    content: [{
      type: 'row',
      content: [{
        type: 'column',
        content: [{
          type: 'component',
          componentName: 'Main',
          isClosable: false,
          tooltip: 'Main - drag to desired position.',
          componentState: {
              cssClass: 'content',
              types: 'untagged',
              updateMethod: 'newlines',
          },
        },
        {
          type: 'component',
          componentName: 'input',
          isClosable: false,
          title: 'Input',
          id: 'inputComponent',
          height: 10,
          tooltip: 'Input - Where you can enter text commands to the server.',
          }]
      },{
      type: 'column',
      content: [{
          type: 'component',
          componentName: 'evennia',
          componentId: 'evennia',
          title: 'Map',
          height: 60,
          isClosable: true,
          componentState: {
            types: 'map',
            updateMethod: 'replace',
          },
      }, {
          type: 'component',
          componentName: 'character_pane',
          componentId: 'character_pane',
          title: 'Character',
          isClosable: false,
          componentState: {
            cssClass: 'content character',
            types: 'character',
            updateMethod: 'replace',
          },
      },{
          type: 'component',
          componentName: 'inventory_pane',
          componentId: 'evennia',
          title: 'Inventory',
          isClosable: false,
          componentState: {
            types: 'inventory',
            updateMethod: 'replace',
          },
        }],
      }],
    }]
  }]
};
