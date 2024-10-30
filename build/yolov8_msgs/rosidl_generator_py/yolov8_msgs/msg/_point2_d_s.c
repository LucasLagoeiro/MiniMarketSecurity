// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from yolov8_msgs:msg/Point2D.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "yolov8_msgs/msg/detail/point2_d__struct.h"
#include "yolov8_msgs/msg/detail/point2_d__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool yolov8_msgs__msg__point2_d__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[34];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("yolov8_msgs.msg._point2_d.Point2D", full_classname_dest, 33) == 0);
  }
  yolov8_msgs__msg__Point2D * ros_message = _ros_message;
  {  // x
    PyObject * field = PyObject_GetAttrString(_pymsg, "x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->x = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // y
    PyObject * field = PyObject_GetAttrString(_pymsg, "y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->y = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // inside
    PyObject * field = PyObject_GetAttrString(_pymsg, "inside");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->inside = (Py_True == field);
    Py_DECREF(field);
  }
  {  // alreadyinside
    PyObject * field = PyObject_GetAttrString(_pymsg, "alreadyinside");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->alreadyinside = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * yolov8_msgs__msg__point2_d__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Point2D */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("yolov8_msgs.msg._point2_d");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Point2D");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  yolov8_msgs__msg__Point2D * ros_message = (yolov8_msgs__msg__Point2D *)raw_ros_message;
  {  // x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // inside
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->inside ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "inside", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // alreadyinside
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->alreadyinside ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "alreadyinside", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}