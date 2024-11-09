import dataclasses
import typing

from fntypes.option import Nothing, Option, Some

import mubble.types
from mubble.node.base import ComposeError, DataNode, ScalarNode
from mubble.node.message import MessageNode


@dataclasses.dataclass(slots=True)
class Attachment(DataNode):
    attachment_type: typing.Literal["audio", "document", "photo", "poll", "video", "successful_payment"]

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
    video: Option[mubble.types.Video] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )
    successful_payment: Option[mubble.types.SuccessfulPayment] = dataclasses.field(
        default_factory=Nothing,
        kw_only=True,
    )

    @classmethod
    def get_attachment_types(cls) -> tuple[typing.Any, ...]:
        return typing.get_args(cls.__annotations__["attachment_type"])

    @classmethod
    def compose(cls, message: MessageNode) -> "Attachment":
        for attachment_type in cls.get_attachment_types():
            match getattr(message, attachment_type, Nothing()):
                case Some(attachment):
                    return cls(attachment_type, **{attachment_type: Some(attachment)})
        return cls.compose_error("No attachment found in message.")


@dataclasses.dataclass(slots=True)
class Photo(DataNode):
    sizes: list[mubble.types.PhotoSize]

    @classmethod
    def compose(cls, attachment: Attachment) -> typing.Self:
        if not attachment.photo:
            raise ComposeError("Attachment is not a photo.")
        return cls(attachment.photo.unwrap())


class Video(ScalarNode, mubble.types.Video):
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Video:
        if not attachment.video:
            raise ComposeError("Attachment is not a video.")
        return attachment.video.unwrap()


class Audio(ScalarNode, mubble.types.Audio):
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Audio:
        if not attachment.audio:
            raise ComposeError("Attachment is not an audio.")
        return attachment.audio.unwrap()


class Document(ScalarNode, mubble.types.Document):
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Document:
        if not attachment.document:
            raise ComposeError("Attachment is not a document.")
        return attachment.document.unwrap()


class Poll(ScalarNode, mubble.types.Poll):
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.Poll:
        if not attachment.poll:
            raise ComposeError("Attachment is not a poll.")
        return attachment.poll.unwrap()


class SuccessfulPayment(ScalarNode, mubble.types.SuccessfulPayment):
    @classmethod
    def compose(cls, attachment: Attachment) -> mubble.types.SuccessfulPayment:
        if not attachment.successful_payment:
            raise ComposeError("Attachment is not a successful payment.")
        return attachment.successful_payment.unwrap()


__all__ = (
    "Attachment",
    "Audio",
    "Document",
    "Photo",
    "Poll",
    "SuccessfulPayment",
    "Video",
)
