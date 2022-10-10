#
# generates ikc group files for csom stacks
#
# TODO:
# add connections between border and submatrix
# change rf etc params to have discrete x and y (no longer symmetric)
from common import *

minlayer=2
maxlayer=4

border_submat_params = \
{
    "AddBorder":["output_x", "output_y", "offset_x", "offset_y"],\
    "Submatrix":["x0", "x1", "y0", "y1"]
}

# read border, submatrix file - used to compensate for
# cropping by spanned csom layers
border_submat_str = readfile("addborder_submatrix.txt")
addborder_str = "$name$_AddBorder"
submat_str = "$name$_Submatrix"

# add span to params
parameter_map.update(parameter_map_span)
# generate string for group module
for i in xrange(minlayer, maxlayer+1):
    output_str = ""
    # add header
    header = ikc_header.replace("$title$", "Group " + csom_name+str(i))
    header = header.replace("$shortdescription$", shortdesc_str.replace("$num$", str(i)))
    header = header.replace("$longdescription$", longdescr_str)
    output_str += header
    output_str += "\n\n"

    # group inputs and outputs
    # TODO dont use parameters, use input and output tags, add to common
    io_str = input_chan_str.replace("$targetmodule$", csom_name + "1")
    io_str = io_str.replace("$target$", "INPUT")
    io_str = io_str.replace("$name$", "INPUT")
    output_str += io_str
    
    io_str = output_chan_str.replace("$sourcemodule$", csom_name + str(i))
    io_str = io_str.replace("$source$", "OUTPUT")
    io_str = io_str.replace("$name$", "OUTPUT")
    output_str += io_str + "\n"

    io_str = output_chan_str.replace("$sourcemodule$", csom_name + "1")
    io_str = io_str.replace("$source$", "RECONSTRUCTION")
    io_str = io_str.replace("$name$", "RECONSTRUCTION")
    output_str += io_str + "\n"

    io_str = output_chan_str.replace("$sourcemodule$", csom_name + str(i))
    io_str = io_str.replace("$source$", "ERROR")
    io_str = io_str.replace("$name$", "ERROR")
    output_str += io_str + "\n"

    # add parameters for group
    output_str += param_comment_str
    for layer_ix in xrange(1, i+1):
        for key in parameter_map.keys():
            for param in parameter_map[key]:
                p_str = param_str.replace("$target$", param)
                p_str = p_str.replace("$module$", csom_name + str(layer_ix))
                p_str = p_str.replace("$name$", csom_name + str(layer_ix) + "_" + param)
                output_str += p_str
        # add for border and submatrix
        if layer_ix < i:
            for key in border_submat_params.keys():
                for param in border_submat_params[key]:
                    p_str = param_str.replace("$target$", param)
                    p_str = p_str.replace("$module$", csom_name + str(layer_ix) + "_" + key)
                    p_str = p_str.replace("$name$", csom_name + str(layer_ix) + "_" + param)
                    output_str += p_str
        output_str += "\n"
    output_str += "\n"

    # add csom modules with border
    output_str += module_comment_str
    for layer_ix in xrange(1, i+1):
        c_str = csom_str.replace("$name$", csom_name + str(layer_ix))
        border_str = ""
        if layer_ix < i:
            border_str = border_submat_str.replace("$name$", csom_name + str(layer_ix))
        output_str += c_str +"\n" + border_str + "\n"
    output_str += "\n"

    # add connections
    output_str += connection_comment_str
    if i > 1:
        for layer_ix in xrange(1, i):
            # add border
            con_str = connection_str.replace("$sourcemodule$", csom_name+str(layer_ix))
            con_str = con_str.replace("$source$", "OUTPUT")
            con_str = con_str.replace("$targetmodule$", addborder_str.replace("$name$", csom_name+str(layer_ix)))
            con_str = con_str.replace("$target$", "INPUT")
            output_str += con_str

            con_str = connection_str.replace("$sourcemodule$", addborder_str.replace("$name$", csom_name+str(layer_ix)))
            con_str = con_str.replace("$source$", "OUTPUT")
            con_str = con_str.replace("$targetmodule$", csom_name+str(layer_ix+1))
            con_str = con_str.replace("$target$", "INPUT")
            output_str += con_str


            # submatrix, remove border
            con_str = connection_str.replace("$sourcemodule$", csom_name+str(layer_ix+1))
            con_str = con_str.replace("$source$", "RECONSTRUCTION")
            con_str = con_str.replace("$targetmodule$", submat_str.replace("$name$", csom_name+str(layer_ix)))
            con_str = con_str.replace("$target$", "INPUT")
            output_str += con_str

            con_str = connection_str.replace("$sourcemodule$", submat_str.replace("$name$", csom_name+str(layer_ix)))
            con_str = con_str.replace("$source$", "OUTPUT")
            con_str = con_str.replace("$targetmodule$", csom_name+str(layer_ix))
            con_str = con_str.replace("$target$", "TOP_DOWN")
            output_str += con_str
            #if layer_ix == i:
        # top modeule should loop back from output
        con_str = connection_str.replace("$sourcemodule$", csom_name+str(i))
        con_str = con_str.replace("$source$", "OUTPUT")
        con_str = con_str.replace("$targetmodule$", csom_name+str(i))
        con_str = con_str.replace("$target$", "TOP_DOWN")

        output_str += con_str
        output_str+="\n"
    elif i == 1:
        con_str = connection_str.replace("$sourcemodule$", csom_name+str(layer_ix))
        con_str = con_str.replace("$source$", "OUTPUT")
        con_str = con_str.replace("$targetmodule$", csom_name+str(layer_ix))
        con_str = con_str.replace("$target$", "TOP_DOWN")
        output_str += con_str + "\n"

    # add test views - show output and weights
    output_str += view_comment_str
    output_str += view_name_str.replace("$name$", csom_name+str(i))
    for layer_ix in xrange(1, i+1):
        v_str = view_str.replace("$module$", csom_name+str(layer_ix))
        v_str = v_str.replace("$source$", "OUTPUT")
        v_str = v_str.replace("$x$", "0")
        v_str = v_str.replace("$y$", str(2*(layer_ix-1)))
        output_str += v_str

        v_str = view_str.replace("$module$", csom_name+str(layer_ix))
        v_str = v_str.replace("$source$", "WEIGHTS")
        v_str = v_str.replace("$x$", "2")
        v_str = v_str.replace("$y$", str(2*(layer_ix-1)))
        output_str += v_str
    # TODO add error view for topmost layer
    v_str = plot_str.replace("$module$", csom_name+str(i))
    v_str = v_str.replace("$source$", "ERROR")
    v_str = v_str.replace("$x$", "0")
    v_str = v_str.replace("$y$", str(2*(i)))
    output_str += v_str

    output_str+="\t</view>\n"
    # add footer
    output_str += ikc_footer

    # save to file
    writefile("../" + csom_name + str(i) + "_group" + ".ikc", output_str)
    # print files
    # print output_str


