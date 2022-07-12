export const tourOptions = {
  defaultStepOptions: {
    cancelIcon: {
      enabled: true
    },
  },
  useModalOverlay: true,
  popperOptions: {
    modifiers: [{ name: 'offset', options: { offset: [0, 24] } }]
  },
};

export const steps = {
  home: [
    {
      id: "create-new-event",
      text: [
        `
        <p>
          Welcome to peFET! To get started, create a new event by telling us it's name and event date!
          Make sure that the name is correct, because it wil be shown to participants! (Don't worry, you can change it later.)
        </p>
        `
      ],
      attachTo: {
        element: '.tour-create-new-event',
        on: 'bottom'
      },
      buttons: [],
    },
  ],
  dashboard: [
    {
      id: "upload-csv",
      text: [
        `
        <p>
          Now that you've created an event, you can add all your participants by uploading a CSV file!
          Just make sure that your file is empty except for two columns, with participant names on the left and their emails on the right!
        </p>
        `
      ],
      attachTo: {
        element: '.tour-upload-csv',
        on: 'bottom'
      },
      buttons: [
        {
          type: 'next',
          text: 'Next'
        }
      ],
    },
    {
      id: "manual-create",
      text: [
        `
        <p>
          On the other hand, if you would like to manually add a participant, you can do so by entering their details and pressing the + button.
        </p>
        `
      ],
      attachTo: {
        element: '.tour-manual-create',
        on: 'bottom'
      },
      buttons: [
        {
          type: 'next',
          text: 'Next'
        }
      ],
    },
    {
      id: "select",
      text: [
        `
        <p>
          Once you're done adding participants, you can start sending them notification emails.
          You can do so by selecting individual participants, or by selecting them all with the checkboxes.
        </p>
        `
      ],
      attachTo: {
        element: '.tour-select',
        on: 'bottom'
      },
      buttons: [
        {
          type: 'next',
          text: 'Next'
        }
      ],
    },
    {
      id: "send-emails",
      text: [
        `
        <p>
          After selecting participants, you can send them emails by clicking on this dropdown menu.
        </p>
        `
      ],
      attachTo: {
        element: '.tour-send-emails',
        on: 'bottom'
      },
      buttons: [
        {
          type: 'next',
          text: 'Next'
        }
      ],
    },
    {
      id: "settings",
      text: [
        `
        <p>
          If you need to make any changes to your event, you can do so in the settings menu.
        </p>
        `
      ],
      attachTo: {
        element: '.tour-settings',
        on: 'right'
      },
      buttons: [
        {
          actionFunc: (tour) => () => tour.complete(),
          text: 'Finish'
        }
      ],
    },
  ]
};
