sap.ui.define([
    "sap/ui/core/UIComponent",
    "sap/sample/bookshop/flaskbookstore/model/models"
], (UIComponent, models) => {
    "use strict";

    return UIComponent.extend("sap.sample.bookshop.flaskbookstore.Component", {
        metadata: {
            manifest: "json",
            interfaces: [
                "sap.ui.core.IAsyncContentCreation"
            ]
        },

        init() {
            // call the base component's init function
            UIComponent.prototype.init.apply(this, arguments);

            // set the device model
            this.setModel(models.createDeviceModel(), "device");

            // enable routing
            this.getRouter().initialize();
        }
    });
});