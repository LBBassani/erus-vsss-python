#ifndef CALIBRACAOARENATHREAD_H
#define CALIBRACAOARENATHREAD_H


#include <QThread>
#include <QTimer>
#include <QImage>
#include <C:\opencv\build\include\opencv2\core\core.hpp>
#include <C:\opencv\build\include\opencv2\highgui\highgui.hpp>

#include "Buffer.h"


class CalibracaoArenaThread : public QThread {
    Q_OBJECT

private:
    Buffer<cv::Mat> *buffer;
    bool m_stop;
    QMutex m_mutex;

protected:
    void run();

public:
    CalibracaoArenaThread(Buffer<cv::Mat> *buffer);
//    ~ColorManagementThread();

signals:
    void newFrame(const cv::Mat &frame);

public slots:
    void stop();
};

#endif // CALIBRACAO_ARENATHREAD

