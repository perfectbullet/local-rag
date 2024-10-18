import sys

from loguru import logger

# remove()方法被首先调用，以删除默认处理程序的配置（其ID为0）。
# 然后，add()方法向记录器添加一个新处理程序。该处理程序将记录到标准错误，只记录INFO或更高级别的日志。
# logger.remove(0)

# TRACE (5): 用于记录程序执行路径的细节信息，以进行诊断。
# DEBUG (10): 开发人员使用该工具记录调试信息。
# INFO (20): 用于记录描述程序正常操作的信息消息。
# SUCCESS (25): 类似于INFO，用于指示操作成功的情况。
# WARNING (30): 警告类型，用于指示可能需要进一步调查的不寻常事件。
# ERROR (40): 错误类型，用于记录影响特定操作的错误条件。
# CRITICAL (50): 严重类型，用于记录阻止核心功能正常工作的错误条件。
# logger.add(sys.stderr, level="DEBUG")
# Loguru还通过其序列化选项支持JSON格式的结构化日志。
# logger.add(sys.stdout, format="{time:YYYY MMMM D HH:mm:ss!UTC} | {level} | {message}")


# 当add函数配置为一个文件时，add方法提供了更多选项来自定义日志文件的处理方式：
# rotate：指定关闭当前日志文件并创建新文件的条件。此条件可以是 int、datetime 或 str，建议使用 str，因为它更易于阅读。
# 如果是整数值，它对应于当前文件在创建新文件之前允许保留的最大字节数。
# 如果是datetime.timedelta 值时，它指示每次旋转的频率，而 datetime.time 指定每个旋转应在一天中发生的时间。
# 如果是str值，这是上述类型的变体。
# retention：指定在从文件系统中删除每个日志文件之前如何保留日志。
# compression：如果设置此选项，日志文件将转换为指定的压缩格式。
# delay：如果设置为 True，则新日志文件的创建将延迟到推送第一条日志消息。
# mode， buffering， encoding： 这些参数将被传递给 Python 的 open（） 函数，该函数决定了 Python 将如何打开日志文件。
logger.add(
    sink="./logs/app.log",
    enqueue=True,
    rotation="4 weeks",
    retention="4 months",
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
    compression="zip",
)


# 输出不同级别的日志消息
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
