# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, \
    ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import setting

Base = declarative_base()
debug = False
engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'
                       % (setting.user_name, setting.password,
                       setting.database_host, setting.database_name,
                       setting.cherset), echo=debug)
Session = sessionmaker(bind=engine)


class PicTopic(Base):

    __tablename__ = 'pic_topics'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    henhen_id = Column(String(255))
    website_type = Column(String(255))
    pic_type = Column(String(255))
    pic_imgs = relationship('PicImg')

    def __init__(
        self,
        title,
        website_type,
        henhen_id,
        pic_type,
        ):

        self.title = title
        self.website_type = website_type
        self.henhen_id = henhen_id
        self.pic_type = pic_type


class PicImg(Base):

    __tablename__ = 'pic_imgs'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    pic_order = Column(Integer)
    pic_topic_id = Column(Integer, ForeignKey('pic_topics.id'))

    def __init__(self, url, pic_order):
        self.url = url
        self.pic_order = pic_order


class VideoTopic(Base):

    __tablename__ = 'video_topics'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    website_type = Column(String(255))
    henhen_id = Column(String(255))
    video_type = Column(String(255))
    video_imgs = relationship('VideoImg')
    video = relationship('Video')

    def __init__(
        self,
        title,
        website_type,
        video_type,
        henhen_id
        ):
        self.title = title
        self.website_type = website_type
        self.video_type = video_type
        self.henhen_id = henhen_id


class VideoImg(Base):

    __tablename__ = 'video_imgs'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    pic_order = Column(Integer)
    video_topic_id = Column(Integer, ForeignKey('video_topics.id'))


class Video(Base):

    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    video_topic_id = Column(Integer, ForeignKey('video_topics.id'))


def get_session():
    return Session()


# create database hspider DEFAULT CHARACTER SET utf8;

def create_tables():
    Base.metadata.create_all(engine)


def save_topic_and_imgs_to_db(class_can_give_info):

    # 先判断图片是否可用

    if not class_can_give_info.is_available():
        return
    title = class_can_give_info.get_title()
    image_url_list = class_can_give_info.get_image_url_list()
    site_inner_id = class_can_give_info.get_site_inner_id()
    website_type = class_can_give_info.get_website_type()
    pic_type = class_can_give_info.get_pic_type()
    session = get_session()
    topic = PicTopic(title, website_type, site_inner_id, pic_type)
    session.add(topic)
    for index in range(0, len(image_url_list)):
        url = image_url_list[index]
        pic = PicImg(url, index)
        session.add(pic)
        topic.pic_imgs.append(pic)
    session.commit()
    session.close()


if __name__ == '__main__':
    create_tables()
