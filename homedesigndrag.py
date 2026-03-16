import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("🏠 AI Architecture Planner")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Plot Setup")

plot_w = st.sidebar.number_input("Plot Width (ft)", 20, 200, 30)
plot_h = st.sidebar.number_input("Plot Length (ft)", 20, 200, 45)

plot_area = plot_w * plot_h

st.subheader("Plot Information")

c1, c2 = st.columns(2)
c1.metric("Plot Area", f"{plot_area} sq ft")
c2.metric("Plot Size", f"{plot_w} x {plot_h} ft")

# -----------------------------
# 2D FLOOR PLANNER
# -----------------------------

canvas = f"""

<div style="display:flex">

<div style="width:260px;border-right:1px solid #ccc;padding:10px">

<h3>Drawing Tools</h3>

<button onclick="wallTool()">Wall</button><br><br>
<button onclick="roomTool()">Room</button><br><br>
<button onclick="doorTool()">Door</button><br><br>
<button onclick="windowTool()">Window</button><br><br>

<h3>Furniture</h3>

<button onclick="bedTool()">Bed</button><br><br>
<button onclick="sofaTool()">Sofa</button><br><br>
<button onclick="tableTool()">Table</button><br><br>

<hr>

<button onclick="selectTool()">Select</button><br><br>
<button onclick="deleteTool()">Delete</button><br><br>
<button onclick="editTool()">Edit</button>

<hr>

<b>Selected Element:</b>
<p id="selectedName">None</p>

</div>

<div id="container"></div>

</div>

<script src="https://unpkg.com/konva@8/konva.min.js"></script>

<script>

var plotWidth = {plot_w}
var plotHeight = {plot_h}

var scale = 12

var width = plotWidth * scale
var height = plotHeight * scale

var stage = new Konva.Stage({{
container:'container',
width:width+100,
height:height+100
}})

var layer = new Konva.Layer()
stage.add(layer)

var transformer = new Konva.Transformer()
layer.add(transformer)

var plot = new Konva.Rect({{
x:50,
y:50,
width:width,
height:height,
stroke:"black",
strokeWidth:4
}})

layer.add(plot)

var currentTool = null
var toolConfig = {{}}

// ---------------- CLICK HANDLER

stage.on('click', function(e){{

var pos = stage.getPointerPosition()

// SELECT

if(currentTool==="select"){{

if(e.target===stage){{
transformer.nodes([])
document.getElementById("selectedName").innerText="None"
return
}}

transformer.nodes([e.target])
var name = e.target.name() || "Element"
document.getElementById("selectedName").innerText=name
}}

// DELETE

else if(currentTool==="delete"){{

if(e.target!==stage){{
var name = e.target.name()

if(confirm("Delete "+name+" ?")){{
e.target.destroy()
layer.draw()
document.getElementById("selectedName").innerText="None"
}}
}}

}}

// EDIT

else if(currentTool==="edit"){{

if(e.target!==stage){{

var group = e.target.getParent()

var color = prompt("New Color")
var w = prompt("New Width (ft)")
var h = prompt("New Height (ft)")

var rect = group.findOne("Rect")

if(rect){{
rect.fill(color)
rect.width(w*scale)
rect.height(h*scale)
}}

var text = group.findOne("Text")

if(text){{
text.text(group.name()+"\\n"+w+" ft x "+h+" ft")
}}

layer.draw()

}}

}}

// WALL

else if(currentTool==="wall"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Wall"
}})

var rect = new Konva.Rect({{
width:toolConfig.length*scale,
height:toolConfig.thickness*scale,
fill:toolConfig.color,
stroke:"black"
}})

var label = new Konva.Text({{
text:"Wall\\n"+toolConfig.length+" ft x "+toolConfig.thickness+" ft",
fontSize:12,
x:5,
y:5
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// ROOM

else if(currentTool==="room"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:toolConfig.name
}})

var rect = new Konva.Rect({{
width:toolConfig.w*scale,
height:toolConfig.h*scale,
fill:toolConfig.color,
stroke:"black"
}})

var label = new Konva.Text({{
text:toolConfig.name+"\\n"+toolConfig.w+" ft x "+toolConfig.h+" ft",
fontSize:14,
x:5,
y:5
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// DOOR

else if(currentTool==="door"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Door"
}})

var rect = new Konva.Rect({{
width:toolConfig.w*scale,
height:toolConfig.h*scale/4,
fill:toolConfig.color
}})

var label = new Konva.Text({{
text:"Door\\n"+toolConfig.w+" ft",
fontSize:12,
x:3,
y:3
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// WINDOW

else if(currentTool==="window"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Window"
}})

var rect = new Konva.Rect({{
width:toolConfig.w*scale,
height:toolConfig.h*scale/4,
fill:toolConfig.color
}})

var label = new Konva.Text({{
text:"Window\\n"+toolConfig.w+" ft",
fontSize:12,
x:3,
y:3
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// BED

else if(currentTool==="bed"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Bed"
}})

var rect = new Konva.Rect({{
width:toolConfig.w*scale,
height:toolConfig.h*scale,
fill:toolConfig.color,
stroke:"black"
}})

var label = new Konva.Text({{
text:"Bed\\n"+toolConfig.w+" ft x "+toolConfig.h+" ft",
fontSize:12,
x:5,
y:5
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// SOFA

else if(currentTool==="sofa"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Sofa"
}})

var rect = new Konva.Rect({{
width:toolConfig.w*scale,
height:toolConfig.h*scale,
fill:toolConfig.color,
stroke:"black"
}})

var label = new Konva.Text({{
text:"Sofa\\n"+toolConfig.w+" ft x "+toolConfig.h+" ft",
fontSize:12,
x:5,
y:5
}})

group.add(rect)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

// TABLE

else if(currentTool==="table"){{

var group = new Konva.Group({{
x:pos.x,
y:pos.y,
draggable:true,
name:"Table"
}})

var circle = new Konva.Circle({{
radius:toolConfig.r*scale,
fill:toolConfig.color,
stroke:"black"
}})

var label = new Konva.Text({{
text:"Table\\n"+toolConfig.r+" ft",
fontSize:12,
x:5,
y:5
}})

group.add(circle)
group.add(label)

layer.add(group)
layer.draw()

currentTool=null

}}

}})

// ---------------- TOOL FUNCTIONS

function wallTool(){{
toolConfig.length = prompt("Wall Length (ft)")
toolConfig.thickness = prompt("Wall Thickness (ft)")
toolConfig.color = prompt("Wall Color")
currentTool="wall"
}}

function roomTool(){{
toolConfig.name = prompt("Room Name")
toolConfig.w = prompt("Width (ft)")
toolConfig.h = prompt("Length (ft)")
toolConfig.color = prompt("Color")
currentTool="room"
}}

function doorTool(){{
toolConfig.w = prompt("Door Width")
toolConfig.h = prompt("Door Height")
toolConfig.color = prompt("Color")
currentTool="door"
}}

function windowTool(){{
toolConfig.w = prompt("Window Width")
toolConfig.h = prompt("Window Height")
toolConfig.color = prompt("Color")
currentTool="window"
}}

function bedTool(){{
toolConfig.w = prompt("Bed Width")
toolConfig.h = prompt("Bed Length")
toolConfig.color = prompt("Color")
currentTool="bed"
}}

function sofaTool(){{
toolConfig.w = prompt("Sofa Width")
toolConfig.h = prompt("Sofa Length")
toolConfig.color = prompt("Color")
currentTool="sofa"
}}

function tableTool(){{
toolConfig.r = prompt("Table Radius")
toolConfig.color = prompt("Color")
currentTool="table"
}}

function selectTool(){{
currentTool="select"
}}

function deleteTool(){{
currentTool="delete"
}}

function editTool(){{
currentTool="edit"
}}

layer.draw()

</script>

"""

components.html(canvas, height=900)