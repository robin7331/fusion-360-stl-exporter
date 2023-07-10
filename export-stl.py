import random
import adsk.core, adsk.fusion, traceback
import os.path, sys


def export_body(body, output_dir, export_mgr, random_name=False):
    fileName = output_dir + "/" + body.name
    if random_name:
        fileName += str(random.randint(0, 1000000))

    stlExportOptions = export_mgr.createSTLExportOptions(body, fileName)
    stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh

    stlExportOptions.sendToPrintUtility = False
    export_mgr.execute(stlExportOptions)


def make_body_name_prefix(project_name):
    # design name
    docName = project_name.rsplit(" ", 1)[0]

    # make docName camel case
    docName = docName.lower()
    docName = docName.replace(" ", "_")
    docName = docName.replace("-", "_")

    return docName


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # get active design
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        if not design:
            ui.messageBox("No active Fusion design", "No Design")
            return

        # Show a message box asking the user if all objects should be exported or just the ones with the name in the project name
        dlg = ui.createFolderDialog()
        dlg.title = "Select a folder to export to"
        dialog_result = dlg.showDialog()
        if dialog_result == adsk.core.DialogResults.DialogOK:
            selected_folder = dlg.folder
            # Process the selected folder
            print("Selected folder:", selected_folder)
        else:
            # User canceled the dialog
            print("Folder selection canceled by user")
            return

        result = ui.messageBox(
            "Include all objects in export?",
            "Export All Objects",
            adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType,
            adsk.core.MessageBoxIconTypes.QuestionIconType,
        )
        exportAll = result == adsk.core.DialogResults.DialogYes

        # get root component in this design
        rootComp = design.rootComponent

        # create a single exportManager instance
        exportMgr = design.exportManager

        # export dir
        stlDir = selected_folder

        # create folder if it does not exist
        if not os.path.exists(stlDir):
            os.makedirs(stlDir)

        # make sure the timeline is at the very end
        design.timeline.moveToEnd()

        # turn the project name e.g. Pixel Pump v251 into pixel_pump
        name_prefix = make_body_name_prefix(rootComp.name)

        exportedFileCount = 0

        # export the body one by one in the design to a specified file
        for body in rootComp.bRepBodies:
            if not body.isVisible:
                continue

            # check if componentName starts with docName so we only export the components we want
            if body.name.startswith(name_prefix):
                # Create a new component using this body.
                newBody = body.createComponent()
                newComp = newBody.parentComponent
                newOcc = design.rootComponent.allOccurrencesByComponent(newBody).item(0)
                export_body(newOcc, stlDir, exportMgr)
                exportedFileCount += 1
            elif exportAll:
                export_body(body, stlDir, exportMgr, True)
                exportedFileCount += 1

        # export the occurrence one by one in the root component to a specified file
        for i in range(0, rootComp.allOccurrences.count):
            occ = rootComp.allOccurrences.item(i)
            bodies = occ.component.bRepBodies
            for body in bodies:
                if not body.isVisible:
                    continue

                if body.name.startswith(name_prefix):
                    export_body(body, stlDir, exportMgr)
                    exportedFileCount += 1
                elif exportAll:
                    export_body(body, stlDir, exportMgr, True)
                    exportedFileCount += 1

        ui.messageBox("Successfully exported {} STL files".format(exportedFileCount))
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))
