#!/usr/bin/env python
#coding=UTF-8
# VMware vSphere Python SDK
# Copyright (c) 2008-2013 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Python program for listing the vms on an ESX / vCenter host
"""

import atexit
import MySQLdb
import datetime

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

import tools.cli as cli
import sys
#reload(sys)                      # reload 才能调用 setdefaultencoding 方法  
#sys.setdefaultencoding('utf-8')  # 设置 'utf-8' 
date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(date)
def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    print "Name       : " , summary.config.name
    print "Guest      : ", summary.config.guestFullName
    print "Instance UUID : ", summary.config.instanceUuid
    print "cpu core : ", summary.config.numCpu
    print "mem size : ", summary.config.memorySizeMB
    print "storage used :", summary.storage.committed
    print "置备的空间:", summary.storage.uncommitted+summary.storage.committed
    print "State      : ", summary.runtime.powerState
    for i in summary.vm.datastore:
      print "LUN       : ", i.name
      print("")
      db_insert_vm_vm_info(summary.config.name,summary.config.instanceUuid,summary.config.numCpu,summary.config.memorySizeMB,summary.storage.uncommitted+summary.storage.committed,summary.storage.committed,i.name)
#    db_insert_vm_vm_info(summary.config.name,summary.config.instanceUuid,summary.config.numCpu,summary.config.memorySizeMB,summary.storage.uncommitted+summary.storage.committed,summary.storage.committed,summary.vm.datastore[0].name)
def print_lun_info(lun):
    summary=lun.summary
    print "Name    :" , summary.name
    print "容量    :" , summary.capacity
    print "free space:" , summary.freeSpace
    db_insert_vm_lun_info(summary.name,summary.capacity,summary.freeSpace)

def db_insert_vm_lun_info(name,capacity,freeSpace):
    db = MySQLdb.connect("localhost", "root", "zhaimingyu", "vm", charset='utf8' )
    cursor = db.cursor()
#    get_lun_id_sql="select id from vm_lun_info where LUN='%s' and DATE='%s' " %(lun,date)
#    cursor.execute(get_lun_id_sql)
#    data = cursor.fetchone()[0]
    sql = "INSERT INTO vm_lun_info(lun,all_space, FREE_SPACE,DATE) VALUES('%s','%d','%d','%s')" %(name,capacity,freeSpace,date)
    try:
      cursor.execute(sql)
      db.commit()
    except:
      db.rollback()
    db.commit()
    cursor.close()
def db_insert_vm_vm_info(name,instance_id,cpu,mem,disk,used_space,lun):
    db = MySQLdb.connect("localhost", "root", "zhaimingyu", "vm", charset='utf8' )
    cursor = db.cursor()
    get_lun_id_sql="select id from vm_lun_info where LUN='%s' and DATE='%s' " %(lun,date)
    cursor.execute(get_lun_id_sql)
    db.commit()
    db.rollback()
    lun_id_data = cursor.fetchone()[0]
    sql ="INSERT INTO vm_vm_info(VM_NAME,VM_ID, VM_CPU,VM_MEM,VM_DISK,VM_USED_SPACE,DATE)VALUES ( '%s', '%s', '%d','%d','%d','%d','%s')"%(name,instance_id,cpu,mem,disk,used_space,date)
    cursor.execute(sql)
    db.commit()
    db.rollback()
    get_vm_id_sql="select max(id) from vm_vm_info"
    cursor.execute(get_vm_id_sql)
    db.commit()
    vm_id_data = cursor.fetchone()[0]
    sql="INSERT INTO vm_vm_info_lun_id(VM_INFO_ID,LUN_INFO_ID)VALUES('%d','%d')"%(vm_id_data,lun_id_data)
    cursor.execute(sql)
    db.commit()
    db.rollback()
    cursor.close()

def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """

    args = cli.get_args()

    try:
        if args.disable_ssl_verification:
            service_instance = connect.SmartConnectNoSSL(host=args.host,
                                                         user=args.user,
                                                         pwd=args.password,
                                                         port=int(args.port))
            print(service_instance)
        else:
            service_instance = connect.SmartConnect(host=args.host,
                                                    user=args.user,
                                                    pwd=args.password,
                                                    port=int(args.port))

        atexit.register(connect.Disconnect, service_instance)

        content = service_instance.RetrieveContent()
#############################################################################
        container = content.rootFolder  # starting point to look into
        viewType = [vim.Datastore]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        children = containerView.view
        for child in children:
            print_lun_info(child)
##############################################################################
        container = content.rootFolder  # starting point to look into
        viewType = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        containerView = content.viewManager.CreateContainerView(
            container, viewType, recursive)

        children = containerView.view
        for child in children:
            print_vm_info(child)
################################################################################
    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0

# Start program
if __name__ == "__main__":
    main()
