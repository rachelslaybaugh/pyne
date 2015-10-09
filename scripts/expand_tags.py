#!/usr/bin/env python

import argparse

from pyne.mesh import Mesh, IMeshTag

def main():
    msg = ("This script reads a mesh (.h5m) file and, for each vector tag of\n"
           "length N, creates N scalar tags. This is useful for visualizing\n"
           "data on mesh with programs that do not support vector tags.\n")
    parser = argparse.ArgumentParser(msg)
    parser.add_argument('mesh_file', help="The path the mesh file")
    parser.add_argument('-o',  dest='output', default='expanded_tags.vtk', 
                        help="The name of the output file")
    parser.add_argument("-t", "--tags", dest='tags', default=None,
                        help=("Instead of expanding all tags, only expand tags\n"
                              "within this list. Tag names listed here should\n"
                              "be seperated by commas without spaces.\n"))
    args = parser.parse_args()

    m = Mesh(structured=True, mesh=args.mesh_file)

    if args.tags is not None:
        tags = args.tags.split(',')
    else:
        tags = []
        for name, tag in m.tags.items():
           if isinstance(tag, IMeshTag) and name != 'idx':
               tags.append(name)

    for tag in tags:
       m.tag = IMeshTag(name=tag)
       m.tag.size = len(m.tag[0])
       if m.tag.size > 1:
           print("Expanding tag: {}".format(tag))
           m.tag.expand()

    print("Saving file {}".format(args.output))
    m.mesh.save(args.output)
    print("Complete")

if __name__ == '__main__':
    main()

