import dataclasses
import typing

from fntypes.option import Nothing, Option, Some

import mubble.types
from mubble.bot.cute_types.message import MessageCute
from mubble.node.base import ComposeError, DataNode, scalar_node

type AttachmentType = typing.Literal[
    "audio",
    "animation",
    "document",
    "photo",
    "poll",
    "voice",
    "video",
    "video_note",
    "successful_payment",
]


@dataclasses.dataclass(slots=True)
class Attachment(DataNode):
    attachment_type: AttachmentType

    animation: Option[mubble.types.Animation] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    audio: Option[mubble.types.Audio] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    document: Option[mubble.types.Document] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    photo: Option[list[mubble.types.PhotoSize]] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    poll: Option[mubble.types.Poll] = dataclasses.field(default_factory=lambda: Nothing(), kw_only=True)
    voice: Option[mubble.types.Voice] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    video: Option[mubble.types.Video] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    video_note: Option[mubble.types.VideoNote] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    successful_payment: Option[mubble.types.SuccessfulPayment] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )

    @classmethod
    def get_attachment_types(cls) -> tuple[AttachmentType, ...]:
        return typing.get_args(AttachmentType.__value__)

    @classmethod
    def compose(cls, message: MessageCute) -> typing.Self:
        for attachment_type in cls.get_attachment_types():
            match getattr(message, attachment_type, Nothing()):
                case Some(attachment):
                    return cls(attachment_type, **{attachment_type: Some(attachment)})
        raise ComposeError("No attachment found in message.")


@dataclasses.dataclass(slots=True)
class Photo(DataNode):
    sizes: list[mubble.types.PhotoSize]

    @classmethod
    def compose(cls, attachment: Attachment) -> typing.Self:
        if not attachment.photo:
            raise ComposeError("Attachment is not a photo.")
        return cls(attachment.photo.unwrap())


@scalar_node
class Video:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Video:
        if not attachment.video:
            raise ComposeError("Attachment is not a video.")
        return attachment.video.unwrap()


@scalar_node
class VideoNote:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.VideoNote:
        if not attachment.video_note:
            raise ComposeError("Attachment is not a video note.")
        return attachment.video_note.unwrap()


@scalar_node
class Audio:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Audio:
        if not attachment.audio:
            raise ComposeError("Attachment is not an audio.")
        return attachment.audio.unwrap()


@scalar_node
class Animation:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Animation:
        if not attachment.animation:
            raise ComposeError("Attachment is not an animation.")
        return attachment.animation.unwrap()


@scalar_node
class Voice:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Voice:
        if not attachment.voice:
            raise ComposeError("Attachment is not a voice.")
        return attachment.voice.unwrap()


@scalar_node
class Document:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Document:
        if not attachment.document:
            raise ComposeError("Attachment is not a document.")
        return attachment.document.unwrap()


@scalar_node
class Poll:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Poll:
        if not attachment.poll:
            raise ComposeError("Attachment is not a poll.")
        return attachment.poll.unwrap()


@scalar_node
class SuccessfulPayment:
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.SuccessfulPayment:
        if not attachment.successful_payment:
            raise ComposeError("Attachment is not a successful payment.")
        return attachment.successful_payment.unwrap()


__all__ = (
    "Animation",
    "Attachment",
    "Audio",
    "Document",
    "Photo",
    "Poll",
    "SuccessfulPayment",
    "Video",
    "VideoNote",
    "Voice",
)
