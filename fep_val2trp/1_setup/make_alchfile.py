#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, copy, optparse
import numpy as np


class ForceField:
    def __init__(self, topfile, parfile):
        self.atoms = {}
        self.bonds = {}
        self.angles = {}
        self.dihedrals = {}
        self.impropers = {}
        self.top = {}
        top_lines = []
        for line in open(topfile):
            top_lines.append(line)
        self.parse_top(top_lines)
        par_lines = []
        for line in open(parfile):
            par_lines.append(line)
        self.parse_par(par_lines)

    def parse_par(self, par_lines):
        flag = ""
        flag_continue = False
        for line in par_lines:
            temp_line_body = line.strip().split("!")[0]
            if not flag_continue:
                line_body = temp_line_body
                if re.search(r"-$", temp_line_body):
                    flag_continue = True
                    continue
            else:
                line_body += temp_line_body
                if re.search(r"-$", temp_line_body):
                    flag_continue = True
                    continue
                else:
                    flag_continue = False
            if re.match(r"BOND|ANGL|DIHE|IMPR|CMAP|NONB", line_body):
                flag = line_body[0:4]
            elif re.match(r"END|HBON", line_body):
                break
            elif len(line_body) == 0:
                pass
            elif flag == "BOND":
                at1, at2, Kb, b0 = line_body.split()[0:4]
                self.bonds[(at1, at2)] = (Kb, b0)
            elif flag == "ANGL":
                at1, at2, at3, Ktheta, Theta0 = line_body.split()[0:5]
                self.angles[(at1, at2, at3)] = (Ktheta, Theta0)
            elif flag == "DIHE":
                at1, at2, at3, at4, Kchi, n, delta = line_body.split()[0:7]
                key = (at1, at2, at3, at4)
                if self.dihedrals.has_key(key):
                    self.dihedrals[(at1, at2, at3, at4)].append((Kchi, n, delta))
                else:
                    self.dihedrals[(at1, at2, at3, at4)] = [(Kchi, n, delta)]
            elif flag == "IMPR":
                at1, at2, at3, at4, Kpsi, n, psi0 = line_body.split()[0:7]
                self.impropers[(at1, at2, at3, at4)] = (Kpsi, psi0)
            elif flag == "CMAP":
                pass
            elif flag == "NONB":
                a = line_body.split()
                if len(a) == 7:
                    at, ign1, eps, rmin2, ign2, eps14, rmin214 = a
                    self.atoms[at] = (eps, rmin2, eps14, rmin214)
                elif len(a) == 4:
                    at, ign1, eps, rmin2 = a
                    self.atoms[at] = (eps, rmin2, "0.0", "0.0")
                else:
                    print "Error"
                    sys.exit(1)

    def parse_top(self, top_lines):
        for line in top_lines:
            if line.startswith("RESI"):
                resname = line[5:9]
                charge = line[19:23]
                self.top[resname] = TopResidue()
            else:
                if line.startswith("ATOM"):
                    a = line.split()
                    self.top[resname].add_atom(a[1], a[2], a[3])
                elif line.startswith("DOUB"):
                    a = line.split()
                    for i in range(1, len(a)-1, 2):
                        self.top[resname].add_double(a[i], a[i+1])
                elif line.startswith("BOND"):
                    a = line.split()
                    for i in range(1, len(a)-1, 2):
                        self.top[resname].add_bond(a[i], a[i+1])
                elif line.startswith("IMPR"):
                    a = line.split()
                    for i in range(1, len(a)-1, 4):
                        self.top[resname].add_improper(a[i], a[i+1], a[i+2], a[i+3])

class TopResidue:
    def __init__(self):
        self.atoms = {}
        self.doubles = []
        self.bonds = []
        self.impropers = []

    def add_atom(self, atmname, atmtype, atmcharge):
        self.atoms[atmname] = (atmtype, atmcharge)

    def add_double(self, atm1, atm2):
        self.doubles.append((atm1, atm2))

    def add_bond(self, atm1, atm2):
        self.bonds.append((atm1, atm2))

    def add_improper(self, atm1, atm2, atm3, atm4):
        self.impropers.append((atm1, atm2, atm3, atm4))

    def remove_duplicate(self):
        bonds_uniq = []
        for bond in self.bonds:
            (atm1, atm2) = bond
            if (atm1, atm2) not in bonds_uniq and (atm2, atm1) not in bonds_uniq:
                bonds_uniq.append((atm1, atm2))
        self.bonds = bonds_uniq
        doubles_uniq = []
        for double in self.doubles:
            (atm1, atm2) = double
            if (atm1, atm2) not in doubles_uniq and (atm2, atm1) not in doubles_uniq:
                doubles_uniq.append((atm1, atm2))
        self.doubles = doubles_uniq
        impropers_uniq = []
        for improper in self.impropers:
            (atm1, atm2, atm3, atm4) = improper
            if (atm1, atm2, atm3, atm4) not in impropers_uniq and (atm4, atm3, atm2, atm1) not in impropers_uniq:
                impropers_uniq.append((atm1, atm2, atm3, atm4))
        self.impropers = impropers_uniq


class Atom:
    def __init__(self, name, resname, resnum, x, y, z, bfactor):
        self.name = name
        self.resname = resname
        self.resnum = resnum
        self.x = x
        self.y = y
        self.z = z
        self.alchflag = bfactor


if __name__ == '__main__':
    op = optparse.OptionParser()
    op.add_option('-f', '--file', dest="input_pdbfile", help=u'PDB file')
    op.add_option('-r', '--resname', dest="new_resname", help=u'New residue name')
    (opts, args) = op.parse_args()
    if not opts.input_pdbfile:
        print u"Error: assign pdbfile."
        print
        op.print_help()
        sys.exit(1)
    elif not opts.new_resname:
        print u"Error: assign new residue name."
        print
        op.print_help()
        sys.exit(1)
    input_pdbfile = opts.input_pdbfile
    new_resname = opts.new_resname
    new_topfile = "%s.top" % opts.new_resname
    new_pdbfile = "%s.pdb" % opts.new_resname

    ## Read forcefield files.
    ff = ForceField("top_all36_cgenff.rtf", "par_all36_cgenff.prm")

    ## Read pdb file.
    ra = []
    rb = []
    ta = {}
    tb = {}
    ncommon = 0
    for line in open(input_pdbfile):
        if line.startswith("ATOM"):
            atmname = line[12:16].strip()
            resname = line[17:21].strip()
            resnum = int(line[22:26])
            x = float(line[30:38])
            y = float(line[38:46])
            z = float(line[46:54])
            bfactor = float(line[60:66])
            if resnum == 1:
                ra_resname = resname
                atm = Atom(atmname, resname, resnum, x, y, z, bfactor)
                if bfactor != 0.0:
                    ta[atmname] = atmname+"A"
                else:
                    ncommon += 1
                ra.append(atm)
            elif resnum == 2:
                rb_resname = resname
                atm = Atom(atmname, resname, resnum, x, y, z, bfactor)
                if bfactor != 0.0:
                    tb[atmname] = atmname+"B"
                rb.append(atm)
    for i in range(ncommon):
        ta[ra[i].name] = ra[i].name
        tb[rb[i].name] = ra[i].name

    ## Construct new topology.
    tr = TopResidue()
    tra = ff.top[ra_resname]
    for atmname in tra.atoms.keys():
        (atmtype, atmcharge) = tra.atoms[atmname]
        tr.add_atom(ta[atmname], atmtype, atmcharge)
    for (atm1, atm2) in tra.bonds:
        tr.add_bond(ta[atm1], ta[atm2])
    for (atm1, atm2) in tra.doubles:
        tr.add_double(ta[atm1], ta[atm2])
    for (atm1, atm2, atm3, atm4) in tra.impropers:
        tr.add_improper(ta[atm1], ta[atm2], ta[atm3], ta[atm4])
    trb = ff.top[rb_resname]
    for atmname in trb.atoms.keys():
        (atmtype, atmcharge) = trb.atoms[atmname]
        tr.add_atom(tb[atmname], atmtype, atmcharge)
    for (atm1, atm2) in trb.bonds:
        tr.add_bond(tb[atm1], tb[atm2])
    for (atm1, atm2) in trb.doubles:
        tr.add_double(tb[atm1], tb[atm2])
    for (atm1, atm2, atm3, atm4) in trb.impropers:
        tr.add_improper(tb[atm1], tb[atm2], tb[atm3], tb[atm4])
    # Remove duplications of bonds, double, and impropers.
    tr.remove_duplicate()

    ## Calculate total charge.
    total_charge = 0.0
    for atmname in tr.atoms.keys():
        (atmtype, atmcharge) = tr.atoms[atmname]
        total_charge += float(atmcharge)

    ## Print new toplogy.
    f = open(new_topfile, "w")
    f.write("RESI %-4s         %4.2f\n" % (new_resname, total_charge))
    for i in range(len(ra)):
        atmname = ta[ra[i].name]
        (atmtype, atmcharge) = tr.atoms[atmname]
        f.write("ATOM %-4s %-6s %6.2f\n" % (atmname, atmtype, float(atmcharge)))
    for i in range(len(rb)):
        if rb[i].alchflag != 0.0:
            atmname = tb[rb[i].name]
            (atmtype, atmcharge) = tr.atoms[atmname]
            f.write("ATOM %-4s %-6s %6.2f\n" % (atmname, atmtype, float(atmcharge)))
    for (atm1, atm2) in tr.bonds:
        f.write("BOND %-4s %-4s\n" % (atm1, atm2))
    for (atm1, atm2) in tr.doubles:
        f.write("DOUBLE %-4s %-4s\n" % (atm1, atm2))
    for (atm1, atm2, atm3, atm4) in tr.impropers:
        f.write("IMPR %-4s %-4s %-4s %-4s\n" % (atm1, atm2, atm3, atm4))
    f.write("END\n")
    f.close()

    ## Print new structure.
    f = open(new_pdbfile, "w")
    j = 1
    for i in range(len(ra)):
        f.write("ATOM  %5d %-4s %-4s %4d    %8.3f%8.3f%8.3f  0.00 %5.2f\n" % (j, ta[ra[i].name], new_resname, 1, ra[i].x, ra[i].y, ra[i].z, ra[i].alchflag))
        j += 1
    for i in range(len(rb)):
        if rb[i].alchflag != 0.0:
            f.write("ATOM  %5d %-4s %-4s %4d    %8.3f%8.3f%8.3f  0.00 %5.2f\n" % (j, tb[rb[i].name], new_resname, 1, rb[i].x, rb[i].y, rb[i].z, rb[i].alchflag))
            j += 1
    f.write("END\n")
    f.close()
