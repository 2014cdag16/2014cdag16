import cherrypy

# 這是 CDAG16 類別的定義
class CDAG16(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
 2014CDA 協同專案下的 cdag16 分組程式開發網頁, 以下為期末報告任務執行內容.<br /><br />
 1. 麻煩先確定下列零件於 V:/home/dumbbell 目錄中,<br />
 並使用 Creo 開啟 V:/home/dumbbell/dumbbell.prt 零件再進行磅數控制.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="design">dumbbell 磅數控制</a><br /><br />

2. Dumbbell 組立成形部分,請再確定下列零件於 V:/home/dumbbell 目錄中<br />
且開啟空白 Creo 組立檔案再進行自動組立.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="assembly">dumbbell 組立</a><br /><br /><br />


<a href="/static/dumbbell">dumbbell.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />

'''
        return outstring
    @cherrypy.expose
    def design(self):
        output = '''
        Select needed dumbbell.<br/>
        <form action='cube1'>
        <input type="text" name="pound">pounds<br>
        <input type="submit" value="Submit">
        </form>
        '''
        return output
    ''' 
    假如採用下列規畫
    
    import programs.cdag16 as cdag16
    root.cdag16 = cdag16.CDAG16()
    
    則程式啟動後, 可以利用 /cdag16/cube1 呼叫函式執行
    '''
    @cherrypy.expose
    def cube1(self , pound, *args, **kwargs):
        '''
    // 假如要自行打開特定零件檔案
    // 若第三輸入為 false, 表示僅載入 session, 但是不顯示
    // ret 為 model open return
    var ret = document.pwl.pwlMdlOpen("dumbbell.prt", "V:/home/dumbbell", false);
    if (!ret.Status) {
        alert("pwlMdlOpen failed (" + ret.ErrorCode + ")");
    }
    //將 ProE 執行階段設為變數 session
    var session = pfcGetProESession();
    // 在視窗中打開零件檔案, 並且顯示出來
    var window = session.OpenFile(pfcCreate("pfcModelDescriptor").CreateFromFileName("dumbbell.prt"));
    var solid = session.GetModel("dumbbell.prt",pfcCreate("pfcModelType").MDL_PART);
        '''
        pound = int(pound)
        w = pound*5
        
        
        outstring = '''      
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcParameterExamples.js"></script>
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcComponentFeatExamples.js"></script>
    </head>
    <body>
    <script type="text/javascript">
var session = pfcGetProESession ();

// 以目前所開啟的檔案為 solid model
// for volume
var solid = session.CurrentModel;

var len, lenVolume, volume, count;
// 將模型檔中的 a 變數設為 javascript 中的 a 變數
len = solid.GetParam("len");

volume=0;
count=0;
try
{

        // 設定變數值, 利用 ModelItem 中的 CreateDoubleParamValue 轉換成 Pro/Web.Link 所需要的浮點數值
    len_Value = pfcCreate ("MpfcModelItem").CreateDoubleParamValue('''+str(w)+''');
    // 將處理好的變數值, 指定給對應的零件變數
    len.Value = len_Value;
    //零件尺寸重新設定後, 呼叫 Regenerate 更新模型
    solid.Regenerate(void null);
    //利用 GetMassProperty 取得模型的質量相關物件
    properties = solid.GetMassProperty(void null);
    volume = properties.Volume;
    alert(volume);
    // 將零件存為新檔案
    //var newfile = document.pwl.pwlMdlSaveAs("filename.prt", "v:/tmp", "filename_5_"+count+".prt");
    // 測試  stl 轉檔
    //var stl_csys = "PRT_CSYS_DEF";
    //var stl_instrs = new pfcCreate ("pfcSTLASCIIExportInstructions").Create(stl_csys);
    //stl_instrs.SetQuality(10);  
    //solid.Export("v:/tmp/filename_5_"+count+".stl", stl_instrs); 
    // 結束測試轉檔
    //if (!newfile.Status) {
            //alert("pwlMdlSaveAs failed (" + newfile.ErrorCode + ")");
        //}
}
catch (err)
{
    alert ("Exception occurred: "+pfcGetExceptionType (err));
}
    </script>
        <form action='index'>
        <input type="submit" value="Previous page">
        </form>
    </body>
    </html>
    '''
        pound = int(pound)
        if pound > 5:
            return outstring
        else:
            return "<h5>Sorry ! Must be larger than 5 pounds !</h5>" + self.design()
        
    @cherrypy.expose
    def fourbar1(self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    </head>
    <body>
<script type="text/javascript">
if (!pfcIsWindows())
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++)
	for (var y = 0; y < 4; y++)
	{
		if (x == y)
			identityMatrix.Set(x, y, 1.0);
		else
			identityMatrix.Set(x, y, 0.0);
	}
// 利用 identityMatrix 建立 transf
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/**----------------------------------------------- link0 -------------------------------------------------------------**/
    //檔案目錄，建議將圖檔放置工作目錄下較方便使用
	var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName("v:/home/fourbar/link0.prt");
	// 若 link1.prt 在 session 則直接取用
	var componentModel = session.GetModelFromDescr(descr);
	// 若 link1.prt 不在 session 則從工作目錄中載入 session
	var componentModel = session.RetrieveModel(descr);
	// 若 link1.prt 已經在 session 則放入組立檔中
	if (componentModel != void null)
	{
		//注意這個 asmcomp 即為設定約束條件的本體
		//asmcomp 為特徵物件, 直接將零件, 以 transf 座標轉換放入組立檔案中
		var asmcomp = assembly.AssembleComponent(componentModel, transf);
	}

// 建立約束條件變數
var constrs = pfcCreate("pfcComponentConstraints");
// 設定組立檔中的三個定位面, 注意內定名稱與 Pro/E WF 中的 ASM_D_FRONT 不同, 而是 ASM_FRONT
// 組立檔案中的 Datum 名稱可以利用 View->plane tag display 查詢名稱
// 建立組立參考面所組成的陣列
var asmDatums = new Array("ASM_FRONT", "ASM_TOP", "ASM_RIGHT");
// 設定零件檔中的三個定位面, 名稱與 Pro/E WF 中相同
var compDatums = new Array("FRONT", "TOP", "RIGHT");
	// 建立 ids 變數, intseq 為 sequence of integers 為資料類別, 使用者可以經由整數索引擷取此資料類別的元件, 第一個索引為 0
           // intseq 等同 Python 的數列資料?
	var ids = pfcCreate("intseq");
	// 建立路徑變數
	var path = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
	// 採用互動式設定相關的變數
	var MpfcSelect = pfcCreate("MpfcSelect");
// 利用迴圈分別約束組立與零件檔中的三個定位平面
for (var i = 0; i < 3; i++)
{
	// 設定組立參考面
	var asmItem = assembly.GetItemByName (pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
	// 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
	if (asmItem == void null)
	{
		interactFlag = true;
		continue;
	}
	// 設定零件參考面
	var compItem = componentModel.GetItemByName (pfcCreate ("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
	// 若無對應的零件參考面, 則啟用互動式平面選擇表單 flag
	if (compItem == void null)
	{
		interactFlag = true;
		continue;
	}
	var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, path);
	var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
	var constr = pfcCreate("pfcComponentConstraint").Create (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
	constr.AssemblyReference = asmSel;
	constr.ComponentReference = compSel;
	constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
	// 將互動選擇相關資料, 附加在程式約束變數之後
	constrs.Append(constr);
}

// 設定組立約束條件
asmcomp.SetConstraints (constrs, void null);
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link1 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link1.prt");
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
            // 注意這個 asmcomp 即為設定約束條件的本體
            // asmcomp 為特徵物件,直接將零件, 以 transf 座標轉換放入組立檔案中
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
// 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
var featID = components.Item(0).Id;

ids.Append(featID);
// 在 assembly 模型中建立子零件所對應的路徑
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array("A_1", "TOP", "ASM_TOP");
var compDatums = new Array("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
// 建立約束條件變數
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
                      // 設定組立參考面, asmItem 為 model item
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
                      // 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
                      // 設定零件參考面, compItem 為 model item
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
                      // 採用互動式設定相關的變數
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
                      // 將互動選擇相關資料, 附加在程式約束變數之後
		constrs.Append(constr);
	}
// 設定組立約束條件, 以 asmcomp 特徵進行約束條件設定
// 請注意, 第二個變數必須為 void null 表示零件對零件進行約束, 若為 subPath, 則零件會與原始零件的平面進行約束
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/

/**----------------------------------------------- link2 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link2.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate ("intseq");
ids.Append(featID+1);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP", "ASM_TOP");
var compDatums = new Array ("A_1", "TOP", "TOP");
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

	
/**-------------------------------------------------------------------------------------------------------------------**/


/**----------------------------------------------- link3 -------------------------------------------------------------**/
var descr = pfcCreate ("pfcModelDescriptor").CreateFromFileName ("v:/home/fourbar/link3.prt");
var componentModel = session.GetModelFromDescr (descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
	var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate ("pfcComponentConstraints");

var ids = pfcCreate ("intseq");
ids.Append(featID+2);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2");
var compDatums = new Array ("A_1");
for (var i = 0; i < 1; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);


var ids = pfcCreate ("intseq");

ids.Append(featID);
var subPath = pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
subassembly = subPath.Leaf;
var asmDatums = new Array ("A_2", "TOP");
var compDatums = new Array ("A_2", "BOTTON");
for (var i = 0; i < 2; i++)
	{
		var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
		if (asmItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
		if (compItem == void null)
		{
			interactFlag = true;
			continue;
		}
		var MpfcSelect = pfcCreate ("MpfcSelect");
		var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
		var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
		var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
		constr.AssemblyReference  = asmSel;
		constr.ComponentReference = compSel;
		constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, true);
		constrs.Append (constr);
	}
asmcomp.SetConstraints (constrs, void null);

/**-------------------------------------------------------------------------------------------------------------------**/

var session = pfcGetProESession ();
var solid = session.CurrentModel;

properties = solid.GetMassProperty(void null);
var COG = properties.GravityCenter;
document.write("MassProperty:<br />");
document.write("Mass:"+(properties.Mass.toFixed(2))+"       pound<br />");
document.write("Average Density:"+(properties.Density.toFixed(2))+"       pound/inch^3<br />");
document.write("Surface area:"+(properties.SurfaceArea.toFixed(2))+"           inch^2<br />");
document.write("Volume:"+(properties.Volume.toFixed(2))+"   inch^3<br />");
document.write("COG_X:"+COG.Item(0).toFixed(2)+"<br />");
document.write("COG_Y:"+COG.Item(1).toFixed(2)+"<br />");
document.write("COG_Z:"+COG.Item(2).toFixed(2)+"<br />");

try
{
document.write("Current Directory:<br />"+currentDir);
}
catch (err)
{
alert ("Exception occurred: "+pfcGetExceptionType (err));
}
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();
</script>
    </body>
    </html>
    '''
        return outstring

    '''
    執行 twentylinks 必須先開一個組立檔案, 放入 link1.prt 之後再執行 Web.Link 程式
    '''
    @cherrypy.expose
    def twentylinks(self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
          if (!pfcIsWindows())
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
      var session = pfcGetProESession();
    // 設定 config option
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣
      var identityMatrix = pfcCreate ("pfcMatrix3D");
      for (var x = 0; x < 4; x++)
        for (var y = 0; y < 4; y++)
          {
        if (x == y)
          identityMatrix.Set (x, y, 1.0);
        else
          identityMatrix.Set (x, y, 0.0);
          }
      var transf = pfcCreate ("pfcTransform3D").Create (identityMatrix);
    // 取得目前的工作目錄
      var currentDir = session.getCurrentDirectory();
    // 以目前已開檔, 作為 model
      var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件
      if (model == void null || model.Type != pfcCreate ("pfcModelType").MDL_ASSEMBLY)
        throw new Error (0, "Current model is not an assembly.");
     
      var assembly = model;
      var descr =
        pfcCreate ("pfcModelDescriptor").CreateFromFileName ("link1.prt");
     for (var partnum = 0; partnum < 20; partnum++)
    {
    // 若 link1.prt 在 session 則直接取用
      var componentModel = session.GetModelFromDescr (descr);
    // 若 link1.prt 不在 session 則從工作目錄中載入 session
      var componentModel = session.RetrieveModel(descr);
    // 若 link1.prt 已經在 session 則放入組立檔中
      if (componentModel != void null)
        {
      var asmcomp = assembly.AssembleComponent (componentModel, transf);
        }
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
      var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    var featID = components.Item(0).Id;
    document.write("目前 featID:"+featID);
    var ids = pfcCreate ("intseq");
    ids.Append(featID+partnum);
    // 在 assembly 模型中建立子零件所對應的路徑
    var subPath =
        pfcCreate ("MpfcAssembly").CreateComponentPath( assembly, ids );
    document.write("id 為:"+subPath.ComponentIds(0));
          subassembly = subPath.Leaf;
    //  設定組立檔中的三個定位面, 注意內定名稱與 Pro/E WF 中的 ASM_D_FRONT 不同, 而是 ASM_FRONT
      var asmDatums = new Array ("A_3", "TOP", "ASM_RIGHT");
    // 設定零件檔中的三個定位面, 名稱與 Pro/E WF 中相同
      var compDatums = new Array ("A_4",
                      "BUTTOM",
                      "RIGHT");
    // 各參考組立關係陣列
      var relation = new Array (pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate ("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
      var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS,pfcCreate("pfcModelItemType").ITEM_SURFACE);
    // 建立約束條件變數
      var constrs = pfcCreate ("pfcComponentConstraints");
     
    // 利用迴圈分別約束組立與零件檔中的三個定位平面
      for (var i = 0; i < 2; i++)
        {
    // 設定組立參考面
          var asmItem =
        subassembly.GetItemByName (relationItem[i],
                    asmDatums [i]);
    // 若無對應的組立參考面, 則啟用互動式平面選擇表單 flag
          if (asmItem == void null)
        {
          interactFlag = true;
          continue;
        }
    // 設定零件參考面
          var compItem =
        componentModel.GetItemByName (relationItem[i],
                          compDatums [i]);
    // 若無對應的零件參考面, 則啟用互動式平面選擇表單 flag
          if (compItem == void null)
        {
          interactFlag = true;
          continue;
        }
    // 採用互動式設定相關的變數
          var MpfcSelect = pfcCreate ("MpfcSelect");
          var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
          var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
          var constr = pfcCreate ("pfcComponentConstraint").Create (relation[i]);
          
          constr.AssemblyReference  = asmSel;
          constr.ComponentReference = compSel;
    // static pfcConstraintAttributes Create (boolean Force, boolean Ignore) 
    // 必須 Force execution of this constraint 才會抑制 comp_placement_assumptions 為 yes 的作動?
          constr.Attributes = pfcCreate ("pfcConstraintAttributes").Create (true, false);
    // 將互動選擇相關資料, 附加在程式約束變數之後
          constrs.Append (constr);
        }
    // 設定組立約束條件
    asmcomp.SetConstraints (constrs, void null);
            try
            {
                      document.write("目前 Creo 的工作目錄:<br />"+currentDir);
                }
        catch (err)
            {
                alert ("Exception occurred: "+pfcGetExceptionType (err));
            }
    }
      assembly.Regenerate (void null);
      session.GetModelWindow (assembly).Repaint();
    </script>
    </body>
    </html>
    '''
        return outstring
        

    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
</head>
<body>
</script><script language="JavaScript">
/*man2.py 完全利用函式呼叫進行組立*/
/*設計一個零件組立函式*/
// featID 為組立件第一個組立零件的編號
// inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
// part2 為外加的零件名稱
////////////////////////////////////////////////
// axis_plane_assembly 組立函式
////////////////////////////////////////////////
function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/dumbbell/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array(axis1, plane1);
var compDatums = new Array(axis2, plane2);
var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 2; i++)
    {
        var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate ("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
        constr.AssemblyReference  = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
        constrs.Append(constr);
    }
asmcomp.SetConstraints(constrs, void null);
}
// 以上為 axis_plane_assembly() 函式
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/dumbbell/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly() 函式



function axis1_plane2_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, plane2, axis2, plane3,plane4){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/dumbbell/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
ids.Append(featID+inc);
var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
subassembly = subPath.Leaf;
var asmDatums = new Array(axis1, plane1,plane2);
var compDatums = new Array(axis2, plane3,plane4);
var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE, pfcCreate("pfcModelItemType").ITEM_SURFACE);
var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate ("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
        constr.AssemblyReference  = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
        constrs.Append(constr);
    }
asmcomp.SetConstraints(constrs, void null);
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////
// three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
///////////////////////////////////////////////////////////////////////////////////////////////////////////
function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
var componentModel = session.GetModelFromDescr(descr);
var componentModel = session.RetrieveModel(descr);
if (componentModel != void null)
{
    var asmcomp = assembly.AssembleComponent (componentModel, transf);
}
var ids = pfcCreate("intseq");
// 若 featID 為 0 表示為空組立檔案
if (featID != 0){
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    }else{
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = assembly;
    // 設法取得第一個組立零件 first_featID
    // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
    var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
    // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
    var first_featID = components.Item(0).Id;
    }
var constrs = pfcCreate("pfcComponentConstraints");
var asmDatums = new Array(plane1, plane2, plane3);
var compDatums = new Array(plane4, plane5, plane6);
var MpfcSelect = pfcCreate("MpfcSelect");
for (var i = 0; i < 3; i++)
{
    var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
    
    if (asmItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
    if (compItem == void null)
    {
        interactFlag = true;
        continue;
    }
    var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
    var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
    var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    constr.AssemblyReference = asmSel;
    constr.ComponentReference = compSel;
    constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
    constrs.Append(constr);
}
asmcomp.SetConstraints(constrs, void null);
// 若 featID = 0 則傳回 first_featID
if (featID == 0)
    return first_featID;
}
// 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows())
// 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions","no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++)
for (var y = 0; y < 4; y++)
{
    if (x == y)
        identityMatrix.Set(x, y, 1.0);
    else
        identityMatrix.Set(x, y, 0.0);
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
throw new Error (0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/////////////////////////////////////////////////////////////////
// 開始執行組立, 全部採函式呼叫組立
/////////////////////////////////////////////////////////////////

// Body 與空組立檔案採三個平面約束組立
// 空組立面為 ASM_TOP, ASM_FRONT, ASM_RIGHT
// Body 組立面為 TOP, FRONT, RIGHT
// 若 featID=0 表示為空組立檔案, 而且函式會傳回第一個組立件的 featID
var featID = three_plane_assembly(session, assembly, transf, 0, 0, "dumbbell_axis.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 
// 利用函式呼叫組立左邊 ARM, 組立增量次序為 1

axis1_plane2_assembly(session, assembly, transf, featID, 0, 
                              "dumbbell.prt", "A_5", "DTM4", "DTM3", "A_4", "DTM3","DTM2");
// 利用函式呼叫組立右邊 ARM, 組立增量次序為 2
axis1_plane2_assembly(session, assembly, transf, featID, 0, 
                              "dumbbell.prt", "A_5", "DTM5", "DTM3", "A_4", "DTM3","DTM2");

// regenerate 並且 repaint 組立檔案
assembly.Regenerate (void null);
session.GetModelWindow (assembly).Repaint();    
</script>
</body>
</html>
'''
        return outstring